import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


def load_data():
    data=pd.read_csv("clean_data.csv")
    print(data.head())    
    
    X=data.drop(columns=["Delivery_Time_min","Order_ID"])
    X=pd.get_dummies(X,drop_first=True)
    y=data["Delivery_Time_min"]
    
    X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42,test_size=0.2)

    













load_data()



