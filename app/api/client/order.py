from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from app.schemas.Order import AddOrder
from app.models.Order import Order
from datetime import datetime
from app.api.auth import get_current_user
from app.schemas.Location import LocationRequest
# from app.models.Location import 
import requests
import os
import openrouteservice

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY").strip()
OPEN_ROUTE_SERVICE=os.getenv("OPEN_ROUTE_SERVICE").strip()

lon=-9.503141
lat=30.348553

client = openrouteservice.Client(key=OPEN_ROUTE_SERVICE)

coords = [
    [-9.5981, 30.4278],  # start (lon, lat)
    [-9.6000, 30.4200]   # end
]
route = client.directions(coords, profile='driving-car')

print(route)

order_router = APIRouter()


 
# @order_router.post('/order')
# def add_order(order: AddOrder, location: LocationRequest, db: Session = Depends(get_db),user=Depends(get_current_user)):
#     url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
#     response=requests.get(url)
#     data=response.json()
#     weather=data["weather"]["main"]
    
    
#     existing_order=db.query(Order).filter(Order.idMeal==order.idMeal).first()
#     # existing_location=db.query(Location.user_id==location.user_id).first()
#     userLocation=Location(
#         user_id= user["user_id"],
#         latitude=location.lat,
#         longitude=location.lng,
#         type="home",
#         created_at=datetime.timezone.utc()
    
#     )
    
#     if (existing_order):
#         raise HTTPException(status_code=400, detail="Order already exist")
#     # if (existing_location):
#     #     raise HTTPException(status_code=400, detail="Order already exist")

#     new_order=Order(
#        idMeal=order.idMeal,
#         user_id= user["user_id"],
#         # created_at=datetime.now(),
#     )
#     db.add(new_order,userLocation)
#     db.commit()
#     db.refresh(new_order,userLocation)
#     return {"message":"order created successfully","id":new_order.idMeal,
#             "longitude":userLocation.longitude,"latitude":userLocation.latitude,
#             "weather":weather
#             }


# @order_router.get('/orders')
# def get_orders(db: Session = Depends(get_db)):
#     orders=db.query(Order).all()
#     return orders

