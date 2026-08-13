def chatbot_response(question, df):
    q = question.lower().strip()

    if any(word in q for word in ["hello", "hi", "hey"]):
        return "Hello! 👋 I can help with popular food, sales, ratings, waste and basic business information."

    if "popular" in q or "best" in q or "top food" in q:
        top = df.groupby("Menu_Item")["Quantity_Sold"].sum().sort_values(ascending=False).head(3)
        items = ", ".join(top.index.tolist())
        return f"The most popular menu items in this dataset are: {items}."

    if "sales" in q:
        return f"Total recorded sales are ৳{df['Total_Sales'].sum():,.0f}. Average order sales are ৳{df['Total_Sales'].mean():,.2f}."

    if "waste" in q:
        return f"Total recorded food waste is {df['Food_Waste'].sum():,.0f} units. You can use the Food Waste Prediction page for an estimate."

    if "rating" in q or "review" in q:
        return f"The average customer rating is {df['Customer_Rating'].mean():.2f} out of 5."

    if "inventory" in q or "stock" in q:
        return "Use the Inventory Prediction page to estimate inventory usage from menu, quantity, branch, day, month and current stock."

    if "thank" in q:
        return "You're welcome! 😊"

    return "I can answer about popular food, sales, inventory, food waste, ratings and reviews. Try asking one of those."

