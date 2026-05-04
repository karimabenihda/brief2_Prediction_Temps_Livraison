from sqlalchemy import Column, String, Integer, DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    idMeal = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
