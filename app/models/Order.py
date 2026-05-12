from sqlalchemy import Column, String, Integer, DateTime,ForeignKey,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    client_id = Column(Integer, ForeignKey("clients.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    delivery_person_id = Column(Integer, ForeignKey("delivery_persons.id"), nullable=True)

    status = Column(String, default="pending")
    total_price = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relations
    restaurant = relationship("Restaurant", back_populates="orders")
    client = relationship("Client", back_populates="orders")
    delivery = relationship("DeliveryPerson", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    meal_id = Column(Integer, ForeignKey("meals.id"))

    quantity = Column(Integer, default=1)
    price = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relations
    order = relationship("Order", back_populates="items")
    meals = relationship("Meal", back_populates="items", cascade="all, delete")    
    
    
class MealType(Base):
    __tablename__ = "meal_types"

    id = Column(Integer, primary_key=True, autoincrement=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relations
    restaurant = relationship("Restaurant", back_populates="meal_types")
    meals = relationship("Meal", back_populates="meal_type")
    
      
class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, autoincrement=True)

    meal_type_id = Column(Integer, ForeignKey("meal_types.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    name = Column(String)
    description = Column(String)
    price = Column(Float)
    available = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relations
    restaurant = relationship("Restaurant", back_populates="meals")
    meal_type = relationship("MealType", back_populates="meals")
    items = relationship("OrderItem", back_populates="meals")
   

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    amount = Column(Float)
    method = Column(String)
    status = Column(String, default="pending")

    order = relationship("Order", back_populates="payments")
    client = relationship("Client", back_populates="payments")
    
