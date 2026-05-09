from fastapi import APIRouter
from app.api.auth import   auth_router
from app.api.client.order import order_router
from app.api.client.prediction import prediction_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(order_router, prefix="/order", tags=["Order"])
api_router.include_router(prediction_router, prefix="/prediction", tags=["Prediction"])