import pandas as pd
from config import BEST_MODEL_MAE

def test_dimension():
    data=pd.read_csv("clean_data.csv")
    X=data.drop(columns="Delivery_Time_min")
    y=data["Delivery_Time_min"]
    assert len(X)==len(y)
    assert BEST_MODEL_MAE<=5.0