from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.core.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    latitude = Column(Float)
    longitude = Column(Float)

    type = Column(String)  # home, work, current
    created_at = Column(DateTime)