from app.api.auth import  auth_router
from app.api.order import order_router
from app.api.prediction import prediction_router

def get_auth_router():
    return auth_router

def get_order_router():
    return order_router

def get_prediction_router():
    return prediction_router
