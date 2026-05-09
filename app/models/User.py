from sqlalchemy import Column, String,Boolean, Integer, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)

    active = Column(Boolean, default=False)
    rights = Column(Integer, default=0)

    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    # relations
    client = relationship("Client", back_populates="user", uselist=False)
    delivery_person = relationship("DeliveryPerson", back_populates="user", uselist=False)
    restaurant = relationship("Restaurant", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    locations = relationship(
        "LocationTrack",
        back_populates="user",
        cascade="all, delete"
    )
    
    
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="client")
    orders = relationship("Order", back_populates="client", cascade="all, delete")
    payments = relationship("Payment", back_populates="client")


class DeliveryPerson(Base):
    __tablename__ = "delivery_persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    vehicle_type = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=False)
    available= Column(Boolean, nullable=False)
    user = relationship("User", back_populates="delivery_person")
    orders = relationship("Order", back_populates="delivery")
    trackings = relationship( "DeliveryTracking", back_populates="delivery_person", cascade="all, delete")

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    birth_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")
    meals = relationship("Meal", back_populates="restaurant")
    meal_types = relationship("MealType", back_populates="restaurant")
    

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    permissions = Column(String)

    user = relationship("User", back_populates="admin")