import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "food_business.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database(csv_path="data/restaurant_business_dataset.csv"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            Order_ID INTEGER PRIMARY KEY,
            Order_Date TEXT, Day_of_Week TEXT, Month INTEGER,
            Customer_ID INTEGER, Menu_Item TEXT, Category TEXT,
            Quantity_Sold INTEGER, Unit_Price REAL, Total_Sales REAL,
            Inventory_Stock INTEGER, Inventory_Used INTEGER, Food_Waste INTEGER,
            Customer_Rating INTEGER, Review TEXT, Sentiment TEXT,
            Payment_Method TEXT, Branch TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            review TEXT NOT NULL,
            rating INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    count = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    if count == 0:
        csv_file = BASE_DIR / csv_path
        df = pd.read_csv(csv_file)
        df.to_sql("orders", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

def load_orders():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    return df

def add_review(customer_name, review, rating):
    conn = get_connection()
    conn.execute(
        "INSERT INTO reviews (customer_name, review, rating) VALUES (?, ?, ?)",
        (customer_name, review, int(rating))
    )
    conn.commit()
    conn.close()

def get_reviews(limit=20):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT customer_name, review, rating, created_at FROM reviews ORDER BY id DESC LIMIT ?",
        conn, params=(int(limit),)
    )
    conn.close()
    return df
