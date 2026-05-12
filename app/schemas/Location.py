from pydantic import BaseModel
from typing import List

class LocationRequest(BaseModel):
    user_id:int
    lat: float
    long: float
    
class LocationDB(BaseModel):
    longitude: List[float]
    latitude: List[float]
    
class LocationRestaurant(BaseModel):
    lat: float
    long: float   
    
      
class LocationDelivery(BaseModel):
    lat: float
    long: float 