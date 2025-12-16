from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager
from app.database import engine, get_db
from app.models import Sensor, Reading, User, Base
from app.schemas import *
from app.mqtt_listener import start_mqtt_listener
from app.auth import hash_password, verify_password, create_access_token, get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    start_mqtt_listener()
    yield

app = FastAPI(
    title="Water Quality Monitoring API",
    description="IoT backend for water quality sensor data",
    version="1.0.0",
    lifespan=lifespan
)

DbSession = Annotated[Session, Depends(get_db)]
UserForm = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
CurrUser = Annotated[User, Depends(get_current_user)]


@app.get("/")
async def root():
    return {"message": "Water Quality API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/sensors", response_model=SensorResponse)
async def create_sensor(sensor: SensorCreate,
                        db: DbSession,
                        current_user: CurrUser # Authenticates current user
                        ):

    db_sensor = Sensor(**sensor.model_dump())
    
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    return db_sensor


@app.get("/sensors", response_model=list[SensorResponse])
async def get_sensors(db: DbSession, current_user: CurrUser):
    sensors = db.query(Sensor).all()
    
    return sensors


@app.get("/sensors/{sensor_id}/stats")
def get_sensor_stats(
    db: DbSession,
    sensor_id: int,
    hours: int = 24  # Last N hours
):
    # Query readings from last N hours
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    # Calculate: avg, min, max, count
    stats = (
        db.query(
            func.round(func.avg(Reading.value)).label("avg"),
            func.min(Reading.value).label("min"),
            func.max(Reading.value).label("max"),
            func.count(Reading.id).label("count"),
        )
        .filter(
            Reading.sensor_id == sensor_id,
            Reading.timestamp >= since,
        )
        .one()
    )
    
    return {
        "sensor_id": sensor_id,
        "hours": hours,
        "average": stats.avg,
        "min": stats.min,
        "max": stats.max,
        "count": stats.count,
    }
    
    
@app.get("/sensors/{sensor_id}/hourly")
def get_hourly_readings(
    db: DbSession,
    sensor_id: int,
    hours: int = 24    
):
    since = datetime.utcnow() - timedelta(hours=hours)

    rows = (
        db.query(
            func.date_trunc("hour", Reading.timestamp).label("hour"),
            func.round(func.avg(Reading.value)).label("avg_value"),
        )
        .filter(
            Reading.sensor_id == sensor_id,
            Reading.timestamp >= since,
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    return [
        {
            "hour": row.hour,
            "average": row.avg_value,
        }
        for row in rows
    ]


@app.post("/readings", response_model=ReadingResponse)
async def create_reading(reading: ReadingCreate,
                        db: DbSession,
                        current_user: CurrUser # Authenticates current user
                        ):
    
    db_reading = Reading(**reading.model_dump())
    
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    return db_reading


@app.get("/readings", response_model=list[ReadingResponse])
async def get_readings(db: DbSession,
                       current_user: CurrUser,
                       sensor_id: int | None = None,
                       limit: int = 100
                       ):
    
    query = db.query(Reading)
    
    if sensor_id:
        query = query.filter(Reading.sensor_id == sensor_id)
    
    readings = query.order_by(Reading.timestamp.desc()).limit(limit).all()
    return readings


@app.post("/register", response_model=UserReponse)
def register(user: UserCreate, db: DbSession):
    # Check if username/email exists
    user_exists = db.query(User).filter(User.username == user.username).first()
    email_exists = db.query(User).filter(User.email == user.email).first()
    
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.post("/token", response_model=Token)
def login(form_data: UserForm, db: DbSession):
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user.username})
    
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}
