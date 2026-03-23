# 🍽️ Uber Eats Bangalore — Restaurant Analytics Dashboard

A decision support system built with Python, SQLite, and Streamlit to analyze Uber Eats Bangalore restaurant data and answer critical business questions using pure SQL queries.

---

## 📌 Project Overview

Uber Eats operates a large-scale restaurant marketplace where business success depends on factors such as location strategy, pricing, cuisine mix, customer ratings, and platform features like online ordering and table booking.

This project analyzes Uber Eats Bangalore restaurant data and presents clean tabular DataFrame outputs in Streamlit — mirroring real internal analytics dashboards where stakeholders require precise tabular insights rather than visual storytelling.

---

## 🛠️ Technical Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core programming language |
| SQLite (sqlite3) | Database — stores restaurant and order data |
| Streamlit | Web application framework |
| Pandas | Data manipulation and SQL result display |

---

## 📁 Project Structure

```
uber_project/
├── uber_ak.csv            # Source restaurant dataset
├── orders.json            # Generated order dataset (JSON format)
├── generate_order.py      # Script to generate orders.json
├── database_setup.py      # Cleans data and loads into SQLite DB
├── uber_data.db           # SQLite database (auto-generated)
├── app.py                 # Streamlit application (3 pages)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 📊 Application Pages

### Page 1 — Dashboard
- Multiple SQL-based filters: Location, Restaurant Type, Online Order, Table Booking, Rating, Cost
- Results displayed as dynamic DataFrame tables
- All filtering logic implemented using SQL WHERE clauses

### Page 2 — Restaurant Q&A
15 business questions answered via SQL queries:

1. Which locations have highest average ratings?
2. Which locations are over-saturated with restaurants?
3. Does online ordering improve ratings?
4. Does table booking correlate with higher ratings?
5. What price range gives best customer satisfaction?
6. How do Low / Mid / Premium restaurants perform?
7. Which cuisines are most common in Bangalore?
8. Which cuisines receive highest average ratings?
9. Which cuisines perform well despite fewer restaurants?
10. What is the relationship between cost and rating?
11. Which locations are ideal for premium onboarding?
12. Which locations have high demand but lower ratings?
13. Do restaurants with both online order + table booking perform better?
14. What combination of factors maximizes restaurant success?
15. Top performers within each pricing segment?

### Page 3 — Orders Q&A
15 order-specific business questions answered via SQL:

1. Total orders, revenue and avg order value
2. Orders by status (Delivered / Cancelled / Pending)
3. Most popular payment methods
4. Top 10 restaurants by number of orders
5. Top 10 restaurants by total revenue
6. Monthly order trend
7. Day-wise order distribution
8. Average delivery time by location
9. Impact of discount on order volume
10. Average customer rating by restaurant
11. Cuisine-wise order count and revenue
12. Location-wise order count and revenue
13. High value orders (above 1000)
14. Best performing restaurants (rating + orders)
15. Cancellation rate by payment method

---

## 🗄️ Database Schema

### Table 1 — restaurants
| Column | Type | Description |
|---|---|---|
| name | TEXT | Restaurant name |
| location | TEXT | Area in Bangalore |
| rest_type | TEXT | Type of restaurant |
| online_order | TEXT | Yes / No |
| book_table | TEXT | Yes / No |
| rate | REAL | Customer rating (0-5) |
| votes | INTEGER | Number of votes |
| approx_cost | INTEGER | Approximate cost for two |
| cuisines | TEXT | Cuisine types |
| price_segment | TEXT | Low / Medium / High |
| rating_category | TEXT | Poor / Average / Excellent |

### Table 2 — orders
| Column | Type | Description |
|---|---|---|
| order_id | TEXT | Unique order ID |
| restaurant_name | TEXT | Restaurant name |
| location | TEXT | Delivery location |
| cuisine | TEXT | Cuisine type |
| order_date | TEXT | Date of order |
| order_month | TEXT | Month name |
| order_day | TEXT | Day of week |
| num_items | INTEGER | Number of items ordered |
| subtotal | INTEGER | Order subtotal |
| delivery_fee | INTEGER | Delivery charges |
| discount_applied | INTEGER | Discount amount |
| total_amount | INTEGER | Final amount paid |
| payment_method | TEXT | UPI / Card / Cash / Wallet |
| order_status | TEXT | Delivered / Cancelled / Pending |
| customer_rating | REAL | Rating given (null if not delivered) |
| delivery_time_min | INTEGER | Delivery time in minutes |

---

## How to Run

### Step 1 — Clone the repository
```bash
git clone https://github.com/your-username/uber_project.git
cd uber_project
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Generate order data
```bash
python generate_order.py
```

### Step 4 — Setup database
```bash
python database_setup.py
```

### Step 5 — Run the app
```bash
streamlit run app.py
```

The app will open automatically at http://localhost:8501

---

## 📈 Key Results

- Identified top-performing and over-saturated locations in Bangalore
- Confirmed that mid-priced restaurants achieve the highest average ratings
- Demonstrated that online ordering and table booking positively impact ratings
- Uncovered cuisine-specific performance and niche opportunities
- Delivered a pure tabular, decision-focused Streamlit application

---

## 📋 Project Evaluation Metrics

- Clean and maintainable Python code
- Modular scripts for scalability
- SQL-driven analytics (no hardcoding)
- Streamlit-based DataFrame outputs only
- Strong alignment with real business decision-making
- GitHub repository with clear documentation

---

## Author

Aravinth
Uber Eats Bangalore Restaurant Analytics Project


