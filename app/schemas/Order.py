from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AddOrder(BaseModel):
    idMeal:int
    user_id:int
    # created_at:datetime