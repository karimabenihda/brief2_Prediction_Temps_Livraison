from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.auth import get_current_user
from app.schemas.Location import LocationRequest,LocationDB,LocationRestaurant,LocationDelivery
from app.models.Location import LocationTrack,DeliveryTracking
import requests
import os
import openrouteservice
from app.schemas.Order import PassOrder,AffectOrder
from app.models.Order import Order,Meal,OrderItem
from app.models.User import Restaurant,DeliveryPerson
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from app.schemas.Order import PassOrder
from app.models.Order import Order
from datetime import datetime
from app.schemas.Prediction import DeliveryPredictionRequest
# from geopy.distance import geodesic


OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY").strip()
OPEN_ROUTE_SERVICE=os.getenv("OPEN_ROUTE_SERVICE").strip()

# lon=-9.503141
# lat=30.348553
 

active_connections = []
order_router = APIRouter()



# @order_router.post('/get_user_location')
def get_user_location(data:LocationRequest):
   return {
        "lat": data.lat,
        "lon": data.long
    }


def get_restaurant_location(
    location:LocationRestaurant,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return {
        "latitude": location.lat,
        "longitude": location.long
    } 
     
   
def get_delivery_location(location:LocationDelivery, db: Session = Depends(get_db),user=Depends(get_current_user)):
    return {
        "latitude": location.lat,
        "longitude": location.long
    }

     
# @order_router.post('/get_coords')
def get_coords(
    user_loc = Depends(get_user_location),
    rest_loc = Depends(get_restaurant_location)
):
    return [user_loc, rest_loc]



# @order_router.post('/get_traffic')
def get_traffic(coords = Depends(get_coords)):
    client = openrouteservice.Client(key=OPEN_ROUTE_SERVICE)
    route = client.directions(
        coordinates=coords,
        profile="driving-car",
        format="json"
    )
    summary = route["routes"][0]["summary"]
    distance = summary["distance"] # meters
    duration = summary["duration"] # seconds
    speed = (distance / duration) * 3.6
    if speed < 15:
        return "High"
    elif speed < 35:
        return "Medium"
    else:
        return "Low"



def get_weather(user_loc = Depends(get_user_location)):
    url=f'https://api.openweathermap.org/data/2.5/weather?lat={user_loc["lat"]}&lon={user_loc["lon"]}&appid={OPENWEATHER_API_KEY}&units=metric'
    response=requests.get(url)
    data=response.json()
    weather=data["weather"]["main"]
    # weather_description = data["weather"][0]["main"]
    return weather




@order_router.websocket("/ws/delivery/{order_id}")
async def delivery_socket(websocket: WebSocket, order_id: int):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            # Validation des données
            if "lat" not in data or "lon" not in data:
                await websocket.send_json({"error": "Données invalides"})
                continue

            location = LocationRequest(
                order_id=order_id,
                latitude=data["lat"],
                longitude=data["lon"]
            )
            # Utilise la fonction existante
            location_data = get_delivery_location(location)

            # Broadcast à tous les clients connectés (sauf l'émetteur)
            for conn in active_connections:
                if conn != websocket:
                    await conn.send_json(location_data)

    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"Erreur : {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)




# @order_router.post('/order/affect_order')
# def affect_order(data: AffectOrder, db: Session = Depends(get_db), user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "READY":
        raise HTTPException(status_code=400, detail="Order not ready for delivery")

    # Récupérer les coordonnées du restaurant
    restaurant = db.query(Restaurant).filter(Restaurant.id == order.restaurant_id).first()
    restaurant_loc = (restaurant.latitude, restaurant.longitude)

    # Récupérer les livreurs disponibles
    deliveries = db.query(DeliveryPerson).filter(DeliveryPerson.longitude != None).all()

    # Calculer la distance entre chaque livreur et le restaurant
    livreurs_distances = []
    for delivery in deliveries:
        delivery_loc = (delivery.latitude, delivery.longitude)
        distance = geodesic(restaurant_loc, delivery_loc).km
        livreurs_distances.append((delivery, distance))

    # Trouver le livreur le plus proche
    if not livreurs_distances:
        raise HTTPException(status_code=400, detail="Aucun livreur disponible")
    delivery, min_distance = min(livreurs_distances, key=lambda x: x[1])

    # Affecter la commande au livreur
    order.delivery_person_id = delivery.id
    order.status = "DELIVERING"
    delivery.is_available = False
    db.commit()

    return {
        "message": "Order assigned successfully",
        "order_id": order.id,
        "delivery_id": delivery.id,
        "status": order.status,
        "distance_km": min_distance
    }


@order_router.post('/create_order')
def create_order(
    order_data: PassOrder, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    # Vérifier les plats
    meals = db.query(Meal).filter(Meal.id.in_(order_data.meals_ids)).all()
    if len(meals) != len(order_data.meals_ids):
        raise HTTPException(status_code=404, detail="Certains plats sont introuvables")

    # Vérifier la disponibilité
    unavailable_meals = [m for m in meals if not m.available]
    if unavailable_meals:
        raise HTTPException(status_code=400, detail=f"Plats indisponibles : {[m.name for m in unavailable_meals]}")

    # Créer la commande
    total_price = sum(meal.price for meal in meals)
    new_order = Order(
        client_id=user["user_id"],
        restaurant_id=order_data.restaurant_id,
        status="pending",
        total_price=total_price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Ajouter les plats
    order_items = [
        OrderItem(order_id=new_order.id, meal_id=meal.id, quantity=1, price=meal.price)
        for meal in meals
    ]
    db.bulk_save_objects(order_items)
    db.commit()

    return {
        "message": "Commande créée",
        "order_id": new_order.id,
        "total_price": total_price,
        "status": new_order.status
    }


@order_router.get('/orders')
def get_orders(db: Session = Depends(get_db)):
    orders=db.query(Order).all()
    return orders

   # restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    # if not restaurant:
    #     raise HTTPException(status_code=404, detail="Restaurant not found")