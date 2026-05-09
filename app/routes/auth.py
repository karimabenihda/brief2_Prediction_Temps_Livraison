from app.api.auth import  auth_router
from app.api.client.order import order_router
from app.api.client.prediction import prediction_router

def get_auth_router():
    return auth_router

def get_order_router():
    return order_router

def get_prediction_router():
    return prediction_router
