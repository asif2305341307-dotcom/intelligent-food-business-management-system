import pandas as pd

REQUIRED_COLUMNS = [
    "Order_ID","Order_Date","Day_of_Week","Month","Customer_ID","Menu_Item",
    "Category","Quantity_Sold","Unit_Price","Total_Sales","Inventory_Stock",
    "Inventory_Used","Food_Waste","Customer_Rating","Review","Sentiment",
    "Payment_Method","Branch"
]

def clean_data(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")

    data = df.copy()
    data = data.drop_duplicates()
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    numeric_cols = [
        "Month","Quantity_Sold","Unit_Price","Total_Sales","Inventory_Stock",
        "Inventory_Used","Food_Waste","Customer_Rating"
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["Review"] = data["Review"].fillna("")
    data["Sentiment"] = data["Sentiment"].fillna("Neutral")
    data = data.dropna(subset=[
        "Order_Date","Day_of_Week","Month","Menu_Item","Category","Branch",
        "Quantity_Sold","Unit_Price","Total_Sales","Inventory_Stock",
        "Inventory_Used","Food_Waste"
    ])
    return data.reset_index(drop=True)
