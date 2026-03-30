import streamlit as st
import pandas as pd
import sqlite3
def get_conn():
    return sqlite3.connect("uber_data.db")
st.set_page_config(
    page_title="Uber Eats Bangalore Analytics",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1.5rem;}
</style>
""", unsafe_allow_html=True)
st.sidebar.title("🍽️ Uber Eats BLR")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "❓ Restaurant Q&A", "📦 Orders Q&A"]
)


if page == "📊 Dashboard":

    st.title("📊 Uber Eats Bangalore — Dashboard")
    st.markdown("Filter restaurant data dynamically using SQL queries.")
    st.markdown("---")

    conn = get_conn()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        locations = pd.read_sql(
            "SELECT DISTINCT location FROM restaurants ORDER BY location", conn
        )['location'].tolist()
        selected_location = st.selectbox("📍 Location", ["All"] + locations)

    with col2:
        rest_types = pd.read_sql(
            "SELECT DISTINCT rest_type FROM restaurants ORDER BY rest_type", conn
        )['rest_type'].tolist()
        selected_type = st.selectbox("🏪 Restaurant Type", ["All"] + rest_types)

    with col3:
        selected_online = st.selectbox("📱 Online Order", ["All", "Yes", "No"])

    with col4:
        selected_booking = st.selectbox("🪑 Table Booking", ["All", "Yes", "No"])

    col5, col6 = st.columns(2)
    with col5:
        min_rating = st.slider("⭐ Min Rating", 0.0, 5.0, 0.0, 0.1)
    with col6:
        max_cost = st.slider("💰 Max Cost (₹)", 100, 3000, 3000, 50)

    conditions = ["1=1"]
    if selected_location != "All":
        conditions.append(f"location = '{selected_location}'")
    if selected_type != "All":
        conditions.append(f"rest_type = '{selected_type}'")
    if selected_online != "All":
        conditions.append(f"online_order = '{selected_online}'")
    if selected_booking != "All":
        conditions.append(f"book_table = '{selected_booking}'")
    conditions.append(f"rate >= {min_rating}")
    conditions.append(f"approx_cost <= {max_cost}")

    where = " AND ".join(conditions)

    query = f"""
        SELECT
            name            AS Restaurant,
            location        AS Location,
            rest_type       AS Type,
            online_order    AS [Online Order],
            book_table      AS [Table Booking],
            rate            AS Rating,
            votes           AS Votes,
            approx_cost     AS [Approx Cost],
            cuisines        AS Cuisines,
            price_segment   AS [Price Segment],
            rating_category AS [Rating Category]
        FROM restaurants
        WHERE {where}
        ORDER BY rate DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    st.markdown(f"### Results — {len(df)} restaurants found")
    st.dataframe(df, use_container_width=True)
elif page == "❓ Restaurant Q&A":

    st.title("❓ Restaurant Business Q&A")
    st.markdown("15 business questions answered using SQL queries.")
    st.markdown("---")

    question = st.selectbox("🔎 Select a Business Question", [
        "Q1.  Which locations have highest average ratings?",
        "Q2.  Which locations are over-saturated with restaurants?",
        "Q3.  Does online ordering improve ratings?",
        "Q4.  Does table booking correlate with higher ratings?",
        "Q5.  What price range gives best customer satisfaction?",
        "Q6.  How do Low / Mid / Premium restaurants perform?",
        "Q7.  Which cuisines are most common in Bangalore?",
        "Q8.  Which cuisines receive highest average ratings?",
        "Q9.  Which cuisines perform well despite fewer restaurants?",
        "Q10. What is the relationship between cost and rating?",
        "Q11. Which locations are ideal for premium onboarding?",
        "Q12. Which locations have high demand but lower ratings?",
        "Q13. Do restaurants with both online order + table booking perform better?",
        "Q14. What combination of factors maximizes restaurant success?",
        "Q15. Top performers within each pricing segment?"
    ])

    conn = get_conn()

    if "Q1" in question:
        st.subheader("📍 Top Locations by Average Rating")
        st.caption("Business Value: Identifies premium areas for brand positioning and partner onboarding.")
        query = """
            SELECT location AS Location,
                   ROUND(AVG(rate), 2)          AS Avg_Rating,
                   COUNT(*)                     AS Total_Restaurants,
                   ROUND(AVG(approx_cost), 0)   AS Avg_Cost
            FROM restaurants
            GROUP BY location
            ORDER BY Avg_Rating DESC
        """

    elif "Q2" in question:
        st.subheader("📍 Over-Saturated Locations")
        st.caption("Business Value: Helps avoid overcrowded markets.")
        query = """
            SELECT location AS Location,
                   COUNT(*)                  AS Total_Restaurants,
                   ROUND(AVG(rate), 2)       AS Avg_Rating,
                   ROUND(AVG(votes), 0)      AS Avg_Votes
            FROM restaurants
            GROUP BY location
            ORDER BY Total_Restaurants DESC
        """

    elif "Q3" in question:
        st.subheader("📱 Online Order Impact on Rating")
        st.caption("Business Value: Evaluates ROI of online ordering feature.")
        query = """
            SELECT online_order              AS Online_Order,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes,
                   ROUND(AVG(approx_cost),0)AS Avg_Cost
            FROM restaurants
            GROUP BY online_order
            ORDER BY Avg_Rating DESC
        """

    elif "Q4" in question:
        st.subheader("🪑 Table Booking Impact on Rating")
        st.caption("Business Value: Measures effectiveness of table booking feature.")
        query = """
            SELECT book_table               AS Table_Booking,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes,
                   ROUND(AVG(approx_cost),0)AS Avg_Cost
            FROM restaurants
            GROUP BY book_table
            ORDER BY Avg_Rating DESC
        """

    elif "Q5" in question:
        st.subheader("💰 Price Range vs Customer Satisfaction")
        st.caption("Business Value: Defines optimal pricing segment for partner success.")
        query = """
            SELECT CASE
                     WHEN approx_cost < 300              THEN 'Low (< 300)'
                     WHEN approx_cost BETWEEN 300 AND 700 THEN 'Mid (300-700)'
                     ELSE                                     'Premium (> 700)'
                   END                      AS Price_Range,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes
            FROM restaurants
            GROUP BY Price_Range
            ORDER BY Avg_Rating DESC
        """

    elif "Q6" in question:
        st.subheader("📊 Low / Mid / Premium Restaurant Performance")
        st.caption("Business Value: Supports pricing-based market segmentation.")
        query = """
            SELECT price_segment            AS Price_Segment,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(MIN(rate), 2)      AS Min_Rating,
                   ROUND(MAX(rate), 2)      AS Max_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes,
                   ROUND(AVG(approx_cost),0)AS Avg_Cost
            FROM restaurants
            GROUP BY price_segment
            ORDER BY Avg_Rating DESC
        """

    elif "Q7" in question:
        st.subheader("🍜 Most Common Cuisines in Bangalore")
        st.caption("Business Value: Reveals market demand and cuisine saturation.")
        query = """
            SELECT cuisines                 AS Cuisine,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating
            FROM restaurants
            GROUP BY cuisines
            ORDER BY Total_Restaurants DESC
            LIMIT 20
        """

    elif "Q8" in question:
        st.subheader("⭐ Highest Rated Cuisines")
        st.caption("Business Value: Identifies high-quality cuisine categories for promotion.")
        query = """
            SELECT cuisines                 AS Cuisine,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes
            FROM restaurants
            GROUP BY cuisines
            HAVING COUNT(*) >= 3
            ORDER BY Avg_Rating DESC
            LIMIT 20
        """

    elif "Q9" in question:
        st.subheader("💎 Niche Cuisines — High Rating, Fewer Restaurants")
        st.caption("Business Value: Highlights niche opportunities for differentiation.")
        query = """
            SELECT cuisines                 AS Cuisine,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes
            FROM restaurants
            GROUP BY cuisines
            HAVING COUNT(*) BETWEEN 1 AND 5
               AND AVG(rate) >= 4.0
            ORDER BY Avg_Rating DESC
            LIMIT 20
        """

    elif "Q10" in question:
        st.subheader("💰 Cost vs Rating Relationship")
        st.caption("Business Value: Does higher pricing mean better customer perception?")
        query = """
            SELECT CASE
                     WHEN approx_cost < 300               THEN 'Low (< 300)'
                     WHEN approx_cost BETWEEN 300 AND 500  THEN 'Mid-Low (300-500)'
                     WHEN approx_cost BETWEEN 500 AND 700  THEN 'Mid-High (500-700)'
                     WHEN approx_cost BETWEEN 700 AND 1000 THEN 'High (700-1000)'
                     ELSE                                      'Premium (> 1000)'
                   END                      AS Cost_Range,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes
            FROM restaurants
            GROUP BY Cost_Range
            ORDER BY Avg_Rating DESC
        """

    elif "Q11" in question:
        st.subheader("🏆 Ideal Locations for Premium Restaurant Onboarding")
        st.caption("Business Value: Combines cost, rating, location for premium expansion.")
        query = """
            SELECT location                 AS Location,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(approx_cost),0)AS Avg_Cost,
                   ROUND(AVG(votes), 0)     AS Avg_Votes
            FROM restaurants
            WHERE price_segment = 'High'
            GROUP BY location
            HAVING AVG(rate) >= 3.8
            ORDER BY Avg_Rating DESC, Avg_Cost DESC
        """

    elif "Q12" in question:
        st.subheader("⚠️ High Demand but Lower Rated Locations")
        st.caption("Business Value: Areas needing quality improvement initiatives.")
        query = """
            SELECT location                 AS Location,
                   COUNT(*)                 AS Total_Restaurants,
                   ROUND(AVG(rate), 2)      AS Avg_Rating,
                   ROUND(AVG(votes), 0)     AS Avg_Votes,
                   ROUND(AVG(approx_cost),0)AS Avg_Cost
            FROM restaurants
            GROUP BY location
            HAVING COUNT(*) >= 10
               AND AVG(rate) < 3.8
            ORDER BY Total_Restaurants DESC
        """

    elif "Q13" in question:
        st.subheader("🔗 Online Order + Table Booking Combo Performance")
        st.caption("Business Value: Validates bundled feature adoption for partners.")
        query = """
            SELECT online_order             AS Online_Order,
                   book_table              AS Table_Booking,
                   COUNT(*)                AS Total_Restaurants,
                   ROUND(AVG(rate), 2)     AS Avg_Rating,
                   ROUND(AVG(votes), 0)    AS Avg_Votes,
                   ROUND(AVG(approx_cost),0)AS Avg_Cost
            FROM restaurants
            GROUP BY online_order, book_table
            ORDER BY Avg_Rating DESC
        """

    elif "Q14" in question:
        st.subheader("🎯 Factors That Maximize Restaurant Success")
        st.caption("Business Value: Supports strategic partner recommendations.")
        query = """
            SELECT online_order             AS Online_Order,
                   book_table              AS Table_Booking,
                   price_segment           AS Price_Segment,
                   COUNT(*)                AS Total_Restaurants,
                   ROUND(AVG(rate), 2)     AS Avg_Rating,
                   ROUND(AVG(votes), 0)    AS Avg_Votes
            FROM restaurants
            GROUP BY online_order, book_table, price_segment
            HAVING COUNT(*) >= 3
            ORDER BY Avg_Rating DESC
            LIMIT 15
        """

    elif "Q15" in question:
        st.subheader("🥇 Top Performers Within Each Pricing Segment")
        st.caption("Business Value: Identifies benchmark partners and best practices.")
        query = """
            SELECT price_segment            AS Price_Segment,
                   name                     AS Restaurant,
                   location                 AS Location,
                   rate                     AS Rating,
                   votes                    AS Votes,
                   approx_cost              AS Cost,
                   cuisines                 AS Cuisines
            FROM restaurants r1
            WHERE rate = (
                SELECT MAX(rate) FROM restaurants r2
                WHERE r2.price_segment = r1.price_segment
            )
            ORDER BY price_segment, Rating DESC
        """

    df = pd.read_sql(query, conn)
    conn.close()

    st.markdown(f"**{len(df)} rows returned**")
    st.dataframe(df, use_container_width=True)
elif page == "📦 Orders Q&A":

    st.title("📦 Orders Data — Business Q&A")
    st.markdown("Order dataset SQL analysis.")
    st.markdown("---")

    question = st.selectbox("🔎 Select an Order Question", [
        "Q1.  Total orders, revenue and avg order value",
        "Q2.  Orders by status (Delivered / Cancelled / Pending)",
        "Q3.  Most popular payment methods",
        "Q4.  Top 10 restaurants by number of orders",
        "Q5.  Top 10 restaurants by total revenue",
        "Q6.  Monthly order trend",
        "Q7.  Day-wise order distribution",
        "Q8.  Average delivery time by location",
        "Q9.  Impact of discount on order volume",
        "Q10. Average customer rating by restaurant",
        "Q11. Cuisine-wise order count and revenue",
        "Q12. Location-wise order count and revenue",
        "Q13. High value orders (above 1000)",
        "Q14. Best performing restaurants (rating + orders)",
        "Q15. Cancellation rate by payment method"
    ])

    conn = get_conn()

    if "Q1" in question:
        st.subheader("📊 Overall Order Summary")
        query = """
            SELECT COUNT(*)                         AS Total_Orders,
                   ROUND(SUM(total_amount), 0)      AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)      AS Avg_Order_Value,
                   ROUND(MIN(total_amount), 0)      AS Min_Order,
                   ROUND(MAX(total_amount), 0)      AS Max_Order,
                   ROUND(AVG(discount_applied), 2)  AS Avg_Discount
            FROM orders
        """

    elif "Q2" in question:
        st.subheader("📋 Orders by Status")
        query = """
            SELECT order_status             AS Status,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(COUNT(*) * 100.0 /
                       (SELECT COUNT(*) FROM orders), 1) AS Percentage,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value
            FROM orders
            GROUP BY order_status
            ORDER BY Total_Orders DESC
        """

    elif "Q3" in question:
        st.subheader("💳 Popular Payment Methods")
        query = """
            SELECT payment_method           AS Payment_Method,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(COUNT(*) * 100.0 /
                       (SELECT COUNT(*) FROM orders), 1) AS Percentage,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value
            FROM orders
            GROUP BY payment_method
            ORDER BY Total_Orders DESC
        """

    elif "Q4" in question:
        st.subheader("🏪 Top 10 Restaurants by Orders")
        query = """
            SELECT restaurant_name          AS Restaurant,
                   location                 AS Location,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value,
                   ROUND(AVG(customer_rating),2) AS Avg_Rating
            FROM orders
            GROUP BY restaurant_name, location
            ORDER BY Total_Orders DESC
            LIMIT 10
        """

    elif "Q5" in question:
        st.subheader("💰 Top 10 Restaurants by Revenue")
        query = """
            SELECT restaurant_name          AS Restaurant,
                   location                 AS Location,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value
            FROM orders
            GROUP BY restaurant_name, location
            ORDER BY Total_Revenue DESC
            LIMIT 10
        """

    elif "Q6" in question:
        st.subheader("📅 Monthly Order Trend")
        query = """
            SELECT order_month              AS Month,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value
            FROM orders
            GROUP BY order_month
            ORDER BY Total_Orders DESC
        """

    elif "Q7" in question:
        st.subheader("📆 Day-wise Order Distribution")
        query = """
            SELECT order_day                AS Day,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value
            FROM orders
            GROUP BY order_day
            ORDER BY Total_Orders DESC
        """

    elif "Q8" in question:
        st.subheader("🚚 Average Delivery Time by Location")
        query = """
            SELECT location                 AS Location,
                   COUNT(*)                 AS Delivered_Orders,
                   ROUND(AVG(delivery_time_min), 1) AS Avg_Delivery_Mins,
                   ROUND(MIN(delivery_time_min), 0) AS Min_Mins,
                   ROUND(MAX(delivery_time_min), 0) AS Max_Mins
            FROM orders
            WHERE order_status = 'Delivered'
              AND delivery_time_min IS NOT NULL
            GROUP BY location
            ORDER BY Avg_Delivery_Mins ASC
        """

    elif "Q9" in question:
        st.subheader("🎁 Discount Impact on Order Volume")
        query = """
            SELECT CASE
                     WHEN discount_applied = 0   THEN 'No Discount'
                     WHEN discount_applied <= 30  THEN 'Low (<=30)'
                     WHEN discount_applied <= 70  THEN 'Mid (31-70)'
                     ELSE                             'High (>70)'
                   END                      AS Discount_Range,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(AVG(total_amount), 2) AS Avg_Order_Value,
                   ROUND(AVG(customer_rating),2) AS Avg_Rating
            FROM orders
            GROUP BY Discount_Range
            ORDER BY Total_Orders DESC
        """

    elif "Q10" in question:
        st.subheader("⭐ Customer Rating by Restaurant")
        query = """
            SELECT restaurant_name          AS Restaurant,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(AVG(customer_rating), 2) AS Avg_Rating,
                   ROUND(MIN(customer_rating), 1) AS Min_Rating,
                   ROUND(MAX(customer_rating), 1) AS Max_Rating
            FROM orders
            WHERE customer_rating IS NOT NULL
            GROUP BY restaurant_name
            HAVING COUNT(*) >= 2
            ORDER BY Avg_Rating DESC
            LIMIT 20
        """

    elif "Q11" in question:
        st.subheader("🍜 Cuisine-wise Orders and Revenue")
        query = """
            SELECT cuisine                  AS Cuisine,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value,
                   ROUND(AVG(customer_rating),2) AS Avg_Rating
            FROM orders
            GROUP BY cuisine
            ORDER BY Total_Orders DESC
        """

    elif "Q12" in question:
        st.subheader("📍 Location-wise Orders and Revenue")
        query = """
            SELECT location                 AS Location,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(total_amount), 2)  AS Avg_Order_Value,
                   ROUND(AVG(customer_rating),2) AS Avg_Rating
            FROM orders
            GROUP BY location
            ORDER BY Total_Orders DESC
        """

    elif "Q13" in question:
        st.subheader("💎 High Value Orders (above 1000)")
        query = """
            SELECT restaurant_name          AS Restaurant,
                   location                 AS Location,
                   cuisine                  AS Cuisine,
                   total_amount             AS Order_Amount,
                   payment_method           AS Payment,
                   order_status             AS Status,
                   customer_rating          AS Rating,
                   order_date               AS Date
            FROM orders
            WHERE total_amount > 1000
            ORDER BY total_amount DESC
            LIMIT 20
        """

    elif "Q14" in question:
        st.subheader("🏆 Best Performing Restaurants")
        query = """
            SELECT restaurant_name          AS Restaurant,
                   location                 AS Location,
                   COUNT(*)                 AS Total_Orders,
                   ROUND(SUM(total_amount), 0)  AS Total_Revenue,
                   ROUND(AVG(customer_rating),2) AS Avg_Rating,
                   ROUND(AVG(delivery_time_min),1) AS Avg_Delivery_Mins
            FROM orders
            WHERE order_status = 'Delivered'
            GROUP BY restaurant_name, location
            HAVING COUNT(*) >= 2
            ORDER BY Avg_Rating DESC, Total_Orders DESC
            LIMIT 15
        """

    elif "Q15" in question:
        st.subheader("❌ Cancellation Rate by Payment Method")
        query = """
            SELECT payment_method           AS Payment_Method,
                   COUNT(*)                 AS Total_Orders,
                   SUM(CASE WHEN order_status = 'Cancelled'
                            THEN 1 ELSE 0 END) AS Cancelled_Orders,
                   ROUND(SUM(CASE WHEN order_status = 'Cancelled'
                            THEN 1 ELSE 0 END) * 100.0
                            / COUNT(*), 1)  AS Cancellation_Rate_Pct
            FROM orders
            GROUP BY payment_method
            ORDER BY Cancellation_Rate_Pct DESC
        """

    df = pd.read_sql(query, conn)
    conn.close()

    st.markdown(f"**{len(df)} rows returned**")
    st.dataframe(df, use_container_width=True)
