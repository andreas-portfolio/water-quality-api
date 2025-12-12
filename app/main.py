from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Sensor, Reading, Base
from app.schemas import *
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Water Quality Monitoring API",
    description="IoT backend for water quality sensor data",
    version="1.0.0",
    lifespan=lifespan
)

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/")
async def root():
    return {"message": "Water Quality API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/sensors", response_model=SensorResponse)
async def create_sensor(sensor: SensorCreate, db: DbSession):
    db_sensor = Sensor(**sensor.model_dump())
    
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    return db_sensor


@app.get("/sensors", response_model=list[SensorResponse])
async def get_sensors(db: DbSession):
    sensors = db.query(Sensor).all()
    
    return sensors
