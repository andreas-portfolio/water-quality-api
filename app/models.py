from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    location = Column(String)
    sensor_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    readings = relationship("Reading", back_populates="sensor")


class Reading(Base):
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    value = Column(Float)
    unit = Column(String)
    
    sensor = relationship("Sensor", back_populates="readings")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    