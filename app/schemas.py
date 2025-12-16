from pydantic import BaseModel
from datetime import datetime


class SensorCreate(BaseModel):
    name: str
    location: str
    sensor_type: str


class SensorResponse(BaseModel):
    id: int
    name: str
    location: str
    sensor_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReadingCreate(BaseModel):
    sensor_id: int
    value: float
    unit: str
    timestamp: datetime | None = None


class ReadingResponse(BaseModel):
    id: int
    sensor_id: int
    timestamp: datetime
    value: float
    unit: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserReponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
