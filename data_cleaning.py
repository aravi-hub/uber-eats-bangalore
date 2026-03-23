import pandas as pd
import json

print("=" * 55)
print("   Uber Eats Bangalore — Data Cleaning Script")
print("=" * 55)

# ─────────────────────────────────────────────────────
# STEP 1 — LOAD RAW CSV
# ─────────────────────────────────────────────────────
print("\n[1/7] Loading raw CSV data...")
df = pd.read_csv("uber_ak.csv")

# Strip trailing commas from column names
df.columns = [c.rstrip(',').strip() for c in df.columns]

print(f"      Rows loaded     : {len(df)}")
print(f"      Columns         : {list(df.columns)}")

# ─────────────────────────────────────────────────────
# STEP 2 — REMOVE DUPLICATES
# ─────────────────────────────────────────────────────
print("\n[2/7] Removing duplicates...")
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)
print(f"      Duplicates removed : {before - after}")
print(f"      Rows remaining     : {after}")

# ─────────────────────────────────────────────────────
# STEP 3 — HANDLE MISSING VALUES
# ─────────────────────────────────────────────────────
print("\n[3/7] Handling missing values...")

# Strip string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip().str.rstrip(',')

# Replace 'nan' strings with actual NaN
df.replace('nan', pd.NA, inplace=True)

# Fill missing text fields
df['name']       = df['name'].fillna('Unknown')
df['location']   = df['location'].fillna('Unknown')
df['cuisines']   = df['cuisines'].fillna('Not Specified')
df['rest_type']  = df['rest_type'].fillna('Not Specified')
df['online_order'] = df['online_order'].fillna('No')
df['book_table']   = df['book_table'].fillna('No')

missing_before = df.isnull().sum().sum()
print(f"      Missing values handled : {missing_before}")

# ─────────────────────────────────────────────────────
# STEP 4 — RATING NORMALIZATION
# ─────────────────────────────────────────────────────
print("\n[4/7] Normalizing ratings...")

# Convert rate to numeric (handles values like '4.1/5', 'NEW', '-' etc.)
df['rate'] = df['rate'].astype(str).str.replace('/5', '').str.strip()
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

# Fill missing ratings with column median
median_rate = df['rate'].median()
df['rate'].fillna(median_rate, inplace=True)

# Clip ratings to valid range 0–5
df['rate'] = df['rate'].clip(0, 5)
df['rate'] = df['rate'].round(2)

print(f"      Rating median used for nulls : {median_rate}")
print(f"      Rating range after clean     : {df['rate'].min()} – {df['rate'].max()}")

# ─────────────────────────────────────────────────────
# STEP 5 — COST STANDARDIZATION
# ─────────────────────────────────────────────────────
print("\n[5/7] Standardizing approx_cost...")

df['approx_cost'] = pd.to_numeric(df['approx_cost'], errors='coerce')

# Fill missing cost with median
median_cost = df['approx_cost'].median()
df['approx_cost'].fillna(median_cost, inplace=True)
df['approx_cost'] = df['approx_cost'].astype(int)

# Standardize votes
df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)

print(f"      Cost median used for nulls : {median_cost}")
print(f"      Cost range after clean     : {df['approx_cost'].min()} – {df['approx_cost'].max()}")

# ─────────────────────────────────────────────────────
# STEP 6 — FEATURE ENGINEERING
# ─────────────────────────────────────────────────────
print("\n[6/7] Feature engineering...")

# Price Segment
def price_segment(cost):
    if cost < 300:
        return 'Low'
    elif cost <= 700:
        return 'Medium'
    else:
        return 'High'

df['price_segment'] = df['approx_cost'].apply(price_segment)

# Rating Category
def rating_category(rate):
    if rate >= 4.0:
        return 'Excellent'
    elif rate >= 3.0:
        return 'Average'
    else:
        return 'Poor'

df['rating_category'] = df['rate'].apply(rating_category)

print(f"      Price segments created     :")
print(df['price_segment'].value_counts().to_string())
print(f"\n      Rating categories created  :")
print(df['rating_category'].value_counts().to_string())

# ─────────────────────────────────────────────────────
# STEP 7 — SAVE CLEANED DATA
# ─────────────────────────────────────────────────────
print("\n[7/7] Saving cleaned data...")

# Keep only required columns
df_clean = df[[
    'name', 'location', 'rest_type', 'online_order', 'book_table',
    'rate', 'votes', 'approx_cost', 'cuisines',
    'listed_in_type', 'listed_in_city',
    'price_segment', 'rating_category'
]].copy()

df_clean.to_csv("uber_ak_cleaned.csv", index=False)

print(f"      Cleaned file saved : uber_ak_cleaned.csv")
print(f"      Final rows         : {len(df_clean)}")
print(f"      Final columns      : {list(df_clean.columns)}")

print("\n" + "=" * 55)
print("   Data Cleaning Complete!")
print("=" * 55)
print("\nNext step: python database_setup.py")