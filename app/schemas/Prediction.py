from pydantic import BaseModel

class DeliveryPredictionRequest(BaseModel):
    Delivery_person_Age: int
    Delivery_person_Ratings: float

    Restaurant_latitude: float
    Restaurant_longitude: float

    Delivery_location_latitude: float
    Delivery_location_longitude: float

    Road_traffic_density: str   # Low / Medium / High / Jam
    Vehicle_condition: int
    multiple_deliveries: int
    Preparation_Duration: int

    Festival: str   # Yes / No / in progress

    Type_of_vehicle: str   # bicycle / scooter / motorcycle / electric_scooter
    Type_of_order: str     # Meal / Snack / Drinks / Buffet

    Weatherconditions: str  # Sunny / Cloudy / Fog / Stormy / ...