import streamlit as st
import pandas as pd

from database import initialize_database, load_orders, add_review, get_reviews
from utils.data_utils import clean_data
from ml_models import train_models, predict_sales, predict_inventory, predict_waste
from nlp_models import train_sentiment_model, predict_sentiment
from recommendation import recommend_items
from chatbot import chatbot_response
from metrics import regression_metrics, classification_metrics

st.set_page_config(page_title="Intelligent Food Business Management", page_icon="🍽️", layout="wide")

DATA_PATH = "data/restaurant_business_dataset.csv"

@st.cache_data
def get_data():
    df = pd.read_csv(DATA_PATH)
    return clean_data(df)

@st.cache_resource
def get_ml_models():
    return train_models(get_data())

@st.cache_resource
def get_nlp_model():
    return train_sentiment_model(get_data())

def main():
    st.title("🍽️ Intelligent Food Business Management System")
    st.caption("Machine Learning + NLP | Restaurant, Homemade Food & Food Cart Management")

    try:
        initialize_database(DATA_PATH)
        df = get_data()
        models = get_ml_models()
        nlp = get_nlp_model()
    except Exception as e:
        st.error(f"Application startup error: {e}")
        st.stop()

    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Go to", [
            "Dashboard", "Sales Prediction", "Inventory Prediction",
            "Food Waste Prediction", "Smart Menu", "Review Sentiment",
            "AI Chatbot", "Data & Reports"
        ])
        st.divider()
        st.info(f"Dataset: {len(df):,} records")

    if page == "Dashboard":
        dashboard(df, models, nlp)
    elif page == "Sales Prediction":
        prediction_page("Sales Prediction", models, df)
    elif page == "Inventory Prediction":
        prediction_page("Inventory Prediction", models, df)
    elif page == "Food Waste Prediction":
        prediction_page("Food Waste Prediction", models, df)
    elif page == "Smart Menu":
        smart_menu(df)
    elif page == "Review Sentiment":
        sentiment_page(df, nlp)
    elif page == "AI Chatbot":
        chatbot_page(df)
    else:
        reports_page(df)

def dashboard(df, models, nlp):
    st.header("📊 Admin Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Orders", f"{len(df):,}")
    c2.metric("Total Sales", f"৳{df['Total_Sales'].sum():,.0f}")
    c3.metric("Food Waste", f"{df['Food_Waste'].sum():,.0f}")
    c4.metric("Average Rating", f"{df['Customer_Rating'].mean():.2f}/5")

    left, right = st.columns(2)
    with left:
        st.subheader("Sales by Month")
        monthly = df.groupby("Month", as_index=False)["Total_Sales"].sum()
        st.bar_chart(monthly.set_index("Month"))
    with right:
        st.subheader("Top Menu Items")
        top = df.groupby("Menu_Item")["Quantity_Sold"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top)

    st.subheader("Sentiment Distribution")
    st.bar_chart(df["Sentiment"].value_counts())

    st.subheader("Model Performance")
    sales_m = regression_metrics(models["sales"], df, "Total_Sales")
    inv_m = regression_metrics(models["inventory"], df, "Inventory_Used")
    waste_m = regression_metrics(models["waste"], df, "Food_Waste")
    sent_m = classification_metrics(nlp, df)
    st.dataframe(pd.DataFrame([
        {"Model":"Sales Prediction", **sales_m},
        {"Model":"Inventory Prediction", **inv_m},
        {"Model":"Food Waste Prediction", **waste_m},
        {"Model":"Sentiment Analysis", **sent_m},
    ]), use_container_width=True)

def prediction_page(kind, models, df):
    st.header(f"🤖 {kind}")
    st.write("Enter simple business information. The trained model will generate an estimate.")
    col1,col2,col3 = st.columns(3)
    with col1:
        menu = st.selectbox("Menu Item", sorted(df["Menu_Item"].unique()))
        branch = st.selectbox("Branch", sorted(df["Branch"].unique()))
        month = st.slider("Month", 1, 12, int(df["Month"].mode()[0]))
    with col2:
        category = st.selectbox("Category", sorted(df["Category"].unique()))
        day = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        quantity = st.number_input("Expected Quantity Sold", 1, 100, 5)
    with col3:
        price = st.number_input("Unit Price (৳)", 1, 5000, int(df.loc[df["Menu_Item"].eq(menu),"Unit_Price"].median()))
        stock = st.number_input("Current Inventory Stock", 0, 500, 20)

    if st.button("Generate Prediction", type="primary"):
        try:
            if kind == "Sales Prediction":
                value = predict_sales(models["sales"], menu, category, branch, day, month, quantity, price)
                st.success(f"Predicted sales: **৳{value:,.2f}**")
            elif kind == "Inventory Prediction":
                value = predict_inventory(models["inventory"], menu, category, branch, day, month, quantity, price, stock)
                st.success(f"Predicted inventory used: **{value:,.0f} units**")
            else:
                value = predict_waste(models["waste"], menu, category, branch, day, month, quantity, price, stock)
                st.warning(f"Predicted food waste: **{value:,.0f} units**")
        except Exception as e:
            st.error(f"Prediction error: {e}")

def smart_menu(df):
    st.header("🍔 Smart Menu Recommendation")
    branch = st.selectbox("Choose Branch", sorted(df["Branch"].unique()))
    category = st.selectbox("Choose Category", ["All"] + sorted(df["Category"].unique()))
    n = st.slider("Number of recommendations", 3, 10, 5)
    if st.button("Recommend Menu", type="primary"):
        recs = recommend_items(df, branch, None if category == "All" else category, n)
        if recs.empty:
            st.warning("No recommendation found.")
        else:
            st.dataframe(recs, use_container_width=True, hide_index=True)

def sentiment_page(df, nlp):
    st.header("💬 Customer Review Sentiment Analysis")
    review = st.text_area("Write a customer review", placeholder="Example: The food was delicious and fresh!")
    if st.button("Analyze Sentiment", type="primary"):
        if not review.strip():
            st.warning("Please enter a review.")
        else:
            label, confidence = predict_sentiment(nlp, review)
            st.success(f"Sentiment: **{label}** | Confidence: **{confidence:.2%}**")

    st.subheader("Recent Reviews")
    st.dataframe(get_reviews(limit=15), use_container_width=True, hide_index=True)

    with st.expander("Add a review to the database"):
        name = st.text_input("Customer name")
        rating = st.slider("Rating", 1, 5, 5)
        if st.button("Save Review"):
            if not review.strip():
                st.warning("Enter review text first.")
            else:
                try:
                    add_review(name.strip() or "Anonymous", review.strip(), rating)
                    st.success("Review saved.")
                except Exception as e:
                    st.error(f"Could not save review: {e}")

def chatbot_page(df):
    st.header("🤖 AI Chatbot")
    st.write("A simple rule-based chatbot for common food-business questions.")
    question = st.text_input("Ask something", placeholder="What is today's popular food?")
    if st.button("Ask Chatbot", type="primary"):
        if not question.strip():
            st.warning("Please type a question.")
        else:
            answer = chatbot_response(question, df)
            st.info(answer)

def reports_page(df):
    st.header("📁 Data & Reports")
    st.subheader("Search Orders")
    query = st.text_input("Search by menu item, category, branch or payment method")
    result = df.copy()
    if query.strip():
        mask = result.astype(str).apply(lambda col: col.str.contains(query, case=False, na=False))
        result = result[mask.any(axis=1)]
    st.dataframe(result.head(500), use_container_width=True, hide_index=True)
    st.caption(f"Showing {min(len(result),500):,} rows out of {len(result):,} matching rows.")

    st.download_button(
        "Download Filtered Report (CSV)",
        data=result.to_csv(index=False).encode("utf-8"),
        file_name="food_business_report.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
