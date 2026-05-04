from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    
    active = Column(Integer,default=0, nullable=True)
    rights = Column(Integer,default=0, nullable=True)

    role = Column(String(50), nullable=False, default="client")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, default=None, nullable=True)
    
    locations = relationship("Location", backref="user")
    orders = relationship("Order",backref="user")
