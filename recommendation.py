import pandas as pd

def recommend_items(df, branch, category=None, n=5):
    data = df[df["Branch"].eq(branch)].copy()
    if category:
        data = data[data["Category"].eq(category)]
    if data.empty:
        return pd.DataFrame()

    result = (
        data.groupby("Menu_Item")
        .agg(
            Orders=("Order_ID","count"),
            Quantity_Sold=("Quantity_Sold","sum"),
            Average_Rating=("Customer_Rating","mean"),
            Total_Sales=("Total_Sales","sum")
        )
        .reset_index()
    )
    # Simple popularity score: sales volume + rating.
    result["Score"] = (
        result["Quantity_Sold"] / max(result["Quantity_Sold"].max(), 1) * 0.7
        + result["Average_Rating"] / 5 * 0.3
    )
    result = result.sort_values(["Score","Quantity_Sold"], ascending=False).head(n)
    result["Average_Rating"] = result["Average_Rating"].round(2)
    result["Score"] = result["Score"].round(3)
    return result
