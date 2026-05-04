from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from app.schemas.Order import AddOrder
from app.models.Order import Order
from datetime import datetime
from app.api.auth import get_current_user
order_router = APIRouter()

@order_router.post('/order')
def add_order(order: AddOrder, db: Session = Depends(get_db),user=Depends(get_current_user)
):
    existing_order=db.query(Order).filter(Order.idMeal==order.idMeal).first()
    if (existing_order):
        raise HTTPException(status_code=400, detail="Order already exist")
    new_order=Order(
       idMeal=order.idMeal,
        user_id= user["user_id"],
        # created_at=datetime.now(),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message":"order created successfully","id":new_order.idMeal}


@order_router.get('/orders')
def get_orders(db: Session = Depends(get_db)):
    orders=db.query(Order).all()
    return orders


