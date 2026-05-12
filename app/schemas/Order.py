from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PassOrder(BaseModel):
    restaurant_id: int
    meals_ids: list[int]
    
    # created_at:datetime
    
class AffectOrder(BaseModel):
    order_id: int
    
    