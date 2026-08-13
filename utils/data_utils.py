import pandas as pd


def clean_data(df):
    df = df.copy()

    # Convert numeric columns
    numeric_columns = [
        "Quantity_Sold",
        "Unit_Price",
        "Total_Sales",
        "Inventory_Used",
        "Food_Waste",
        "Customer_Rating",
        "Month"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows missing important values
    important_columns = [
        "Menu_Item",
        "Category",
        "Branch",
        "Day_of_Week"
    ]

    existing_columns = [c for c in important_columns if c in df.columns]

    if existing_columns:
        df = df.dropna(subset=existing_columns)

    # Fill missing numeric values
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Create Month if it does not exist
    if "Month" not in df.columns:
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df["Month"] = df["Date"].dt.month

    return df
