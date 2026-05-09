from pydantic import BaseModel


class LocationRequest(BaseModel):
    user_id:int
    lat: float
    lng: float