import sqlite3
import pandas as pd
import json
import ast

print("=" * 50)
print("   Uber Eats - Database Setup")
print("=" * 50)

# ── Connect to SQLite ──
conn   = sqlite3.connect("uber_data.db")
cursor = conn.cursor()
print("\n[1/4] Connected to uber_data.db")

# ════════════════════════════════════════════════
# TABLE 1 — restaurants  (from uber_ak.csv)
# ════════════════════════════════════════════════
cursor.execute("DROP TABLE IF EXISTS restaurants")
cursor.execute("""
CREATE TABLE restaurants (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT,
    online_order    TEXT,
    book_table      TEXT,
    rate            REAL,
    votes           INTEGER,
    location        TEXT,
    rest_type       TEXT,
    cuisines        TEXT,
    approx_cost     INTEGER,
    listed_in_type  TEXT,
    price_segment   TEXT,
    rating_category TEXT
)
""")

# ── Load cleaned CSV (output of data_cleaning.py) ──
df = pd.read_csv("uber_ak_cleaned.csv")
df['rate']        = pd.to_numeric(df['rate'],        errors='coerce').fillna(0)
df['votes']       = pd.to_numeric(df['votes'],       errors='coerce').fillna(0).astype(int)
df['approx_cost'] = pd.to_numeric(df['approx_cost'], errors='coerce').fillna(0).astype(int)

# ── Insert restaurants ──
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO restaurants
        (name, online_order, book_table, rate, votes, location,
         rest_type, cuisines, approx_cost, listed_in_type, price_segment, rating_category)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        row.get('name'),
        row.get('online_order'),
        row.get('book_table'),
        row.get('rate'),
        row.get('votes'),
        row.get('location'),
        row.get('rest_type'),
        row.get('cuisines'),
        row.get('approx_cost'),
        row.get('listed_in_type'),
        row.get('price_segment'),
        row.get('rating_category')
    ))

print(f"[2/4] restaurants table created — {len(df)} rows inserted")

# ════════════════════════════════════════════════
# TABLE 2 — orders  (from orders.json)
# ════════════════════════════════════════════════
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("""
CREATE TABLE orders (
    order_id            TEXT PRIMARY KEY,
    restaurant_name     TEXT,
    location            TEXT,
    cuisine             TEXT,
    order_date          TEXT,
    order_month         TEXT,
    order_day           TEXT,
    items_ordered       TEXT,
    num_items           INTEGER,
    subtotal            INTEGER,
    delivery_fee        INTEGER,
    discount_applied    INTEGER,
    total_amount        INTEGER,
    payment_method      TEXT,
    order_status        TEXT,
    customer_rating     REAL,
    delivery_time_min   INTEGER
)
""")

# ── Load orders.json ──
with open("orders.json", "r") as f:
    orders = json.load(f)

for o in orders:
    # items_ordered is a list — store as comma-separated string
    items_str = ", ".join(o.get("items_ordered", []))
    cursor.execute("""
        INSERT INTO orders
        (order_id, restaurant_name, location, cuisine, order_date,
         order_month, order_day, items_ordered, num_items, subtotal,
         delivery_fee, discount_applied, total_amount, payment_method,
         order_status, customer_rating, delivery_time_min)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        o.get("order_id"),
        o.get("restaurant_name"),
        o.get("location"),
        o.get("cuisine"),
        o.get("order_date"),
        o.get("order_month"),
        o.get("order_day"),
        items_str,
        o.get("num_items"),
        o.get("subtotal"),
        o.get("delivery_fee"),
        o.get("discount_applied"),
        o.get("total_amount"),
        o.get("payment_method"),
        o.get("order_status"),
        o.get("customer_rating"),
        o.get("delivery_time_min")
    ))

print(f"[3/4] orders table created     — {len(orders)} rows inserted")

# ── Save ──
conn.commit()
conn.close()
print("[4/4] uber_data.db saved successfully!")

print("\n" + "=" * 50)
print("   Setup Complete!")
print("=" * 50)
print("\nTables created:")
print("  restaurants  — restaurant data from CSV")
print("  orders       — order data from JSON")
print("\nNext step: streamlit run app.py")