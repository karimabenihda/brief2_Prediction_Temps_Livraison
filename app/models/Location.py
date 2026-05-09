from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class LocationTrack(Base):
    __tablename__ = "locations_track"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    location_type = Column(String)  # home, work, current

    created_at = Column(DateTime, default=datetime.utcnow)

    # relation
    user = relationship("User", back_populates="locations")
    
    
class DeliveryTracking(Base):
    __tablename__ = "delivery_tracking"

    id = Column(Integer, primary_key=True, autoincrement=True)

    delivery_person_id = Column(Integer, ForeignKey("delivery_persons.id"), index=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relation
    delivery_person = relationship("DeliveryPerson", back_populates="trackings")