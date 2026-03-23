import json
import random
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv("uber_ak.csv")
df.columns = [c.rstrip(',').strip() for c in df.columns]
restaurant_names = df['name'].dropna().unique().tolist()
locations        = df['location'].dropna().unique().tolist()

payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Wallet"]
order_statuses  = ["Delivered", "Delivered", "Delivered", "Cancelled", "Pending"]
cuisines_list   = ["North Indian", "South Indian", "Chinese", "Italian",
                   "Fast Food", "Cafe", "Biryani", "Continental", "Mexican", "Thai"]
menu_items      = ["Butter Naan", "Dal Makhani", "Chicken Biryani", "Paneer Butter Masala",
                   "Margherita Pizza", "Hakka Noodles", "Masala Dosa", "Tandoori Chicken",
                   "Garlic Bread", "Fried Rice", "Momos", "Chole Bhature",
                   "Veg Fried Rice", "Mutton Biryani", "Pasta Arrabiata",
                   "Gulab Jamun", "Chicken Tikka", "Chocolate Brownie",
                   "Spring Rolls", "Burgers"]

def random_date():
    start    = datetime(2024, 1, 1)
    end      = datetime(2024, 12, 31)
    rand_day = start + timedelta(days=random.randint(0, (end - start).days))
    return rand_day.strftime("%Y-%m-%d"), rand_day.strftime("%B"), rand_day.strftime("%A")

orders = []
for i in range(1, 501):
    status = random.choice(order_statuses)
    date_str, month, day = random_date()
    items        = random.sample(menu_items, random.randint(1, 4))
    subtotal     = random.randint(100, 1500)
    delivery_fee = random.choice([0, 30, 49, 59])
    discount     = random.choice([0, 0, 0, 20, 50, 100])
    total        = max(subtotal + delivery_fee - discount, 50)

    orders.append({
        "order_id"          : f"ORD{i:04d}",
        "restaurant_name"   : random.choice(restaurant_names),
        "location"          : random.choice(locations),
        "cuisine"           : random.choice(cuisines_list),
        "order_date"        : date_str,
        "order_month"       : month,
        "order_day"         : day,
        "items_ordered"     : items,
        "num_items"         : len(items),
        "subtotal"          : subtotal,
        "delivery_fee"      : delivery_fee,
        "discount_applied"  : discount,
        "total_amount"      : total,
        "payment_method"    : random.choice(payment_methods),
        "order_status"      : status,
        "customer_rating"   : round(random.uniform(2.5, 5.0), 1) if status == "Delivered" else None,
        "delivery_time_min" : random.randint(20, 90) if status == "Delivered" else None
    })

with open("orders.json", "w") as f:
    json.dump(orders, f, indent=2)

statuses = {}
for o in orders:
    statuses[o['order_status']] = statuses.get(o['order_status'], 0) + 1

print("=" * 40)
print("  orders.json created successfully!")
print("=" * 40)
print(f"  Total    : 500 orders")
print(f"  Delivered: {statuses.get('Delivered', 0)}")
print(f"  Cancelled: {statuses.get('Cancelled', 0)}")
print(f"  Pending  : {statuses.get('Pending',   0)}")
print("=" * 40)