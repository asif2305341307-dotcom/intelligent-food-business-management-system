import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

CAT_COLS = ["Menu_Item","Category","Branch","Day_of_Week"]
SALES_FEATURES = CAT_COLS + ["Month","Quantity_Sold","Unit_Price"]
INV_FEATURES = CAT_COLS + ["Month","Quantity_Sold","Unit_Price","Inventory_Stock"]
WASTE_FEATURES = CAT_COLS + ["Month","Quantity_Sold","Unit_Price","Inventory_Stock"]

def _make_model():
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
    ], remainder="passthrough")
    model = RandomForestRegressor(
        n_estimators=150, random_state=42, min_samples_leaf=2, n_jobs=-1
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])

def _train_one(df, features, target):
    X = df[features].copy()
    y = df[target].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    model = _make_model()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = {
        "MAE": round(float(mean_absolute_error(y_test, pred)), 2),
        "RMSE": round(float(np.sqrt(mean_squared_error(y_test, pred))), 2),
        "R2": round(float(r2_score(y_test, pred)), 3),
    }
    return model, metrics

def train_models(df):
    sales_model, sales_metrics = _train_one(df, SALES_FEATURES, "Total_Sales")
    inv_model, inv_metrics = _train_one(df, INV_FEATURES, "Inventory_Used")
    waste_model, waste_metrics = _train_one(df, WASTE_FEATURES, "Food_Waste")
    return {
        "sales": {"model": sales_model, "metrics": sales_metrics},
        "inventory": {"model": inv_model, "metrics": inv_metrics},
        "waste": {"model": waste_model, "metrics": waste_metrics},
    }

def _row(menu, category, branch, day, month, quantity, price, stock):
    return pd.DataFrame([{
        "Menu_Item": menu, "Category": category, "Branch": branch,
        "Day_of_Week": day, "Month": month, "Quantity_Sold": quantity,
        "Unit_Price": price, "Inventory_Stock": stock
    }])

def predict_sales(bundle, menu, category, branch, day, month, quantity, price):
    value = float(bundle["model"].predict(
        _row(menu, category, branch, day, month, quantity, price, 0)
    )[0])
    return max(0.0, value)

def predict_inventory(bundle, menu, category, branch, day, month, quantity, price, stock):
    value = float(bundle["model"].predict(
        _row(menu, category, branch, day, month, quantity, price, stock)
    )[0])
    return max(0.0, value)

def predict_waste(bundle, menu, category, branch, day, month, quantity, price, stock):
    value = float(bundle["model"].predict(
        _row(menu, category, branch, day, month, quantity, price, stock)
    )[0])
    return max(0.0, value)
