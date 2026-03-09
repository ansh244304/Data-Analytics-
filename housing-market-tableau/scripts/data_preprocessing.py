"""
data_preprocessing.py
----------------------
Cleans and prepares the raw housing dataset for analysis and Tableau export.

Run from project root:
    python scripts/data_preprocessing.py
"""

import pandas as pd
import numpy as np
import os
import glob

# ── 1. Load Data ────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Find the CSV file (kagglehub may name it differently)
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
if not csv_files:
    raise FileNotFoundError(
        "No CSV file found in /data. "
        "Run  python data/download_data.py  first."
    )

raw_path = csv_files[0]
print(f"Loading: {raw_path}")
df = pd.read_csv(raw_path)

print(f"\nRaw shape: {df.shape}")
print(df.head())
print("\nColumn dtypes:\n", df.dtypes)
print("\nNull counts:\n", df.isnull().sum())

# ── 2. Standardise Column Names ─────────────────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^\w]", "_", regex=True)
)
print("\nStandardised columns:", df.columns.tolist())

# ── 3. Drop Duplicates ──────────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
print(f"\nDropped {before - len(df)} duplicate rows.")

# ── 4. Handle Missing Values ────────────────────────────────────────────────
# Numeric columns → fill with median
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
for col in num_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)

# Categorical columns → fill with mode
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
for col in cat_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)

# ── 5. Derive Useful Columns ────────────────────────────────────────────────

# House Age (assumes a 'yr_built' column; adjust name if different)
CURRENT_YEAR = 2024
if "yr_built" in df.columns:
    df["house_age"] = CURRENT_YEAR - df["yr_built"]

# Years Since Renovation
if "yr_renovated" in df.columns:
    df["renovated"] = df["yr_renovated"].apply(lambda x: "Renovated" if x > 0 else "Not Renovated")
    df["yr_since_renovation"] = df["yr_renovated"].apply(
        lambda x: CURRENT_YEAR - x if x > 0 else CURRENT_YEAR - df["yr_built"].mean()
    )

# Price Bins for histogram
if "price" in df.columns:
    df["price_bin"] = pd.cut(
        df["price"],
        bins=[0, 200000, 400000, 600000, 800000, 1000000, float("inf")],
        labels=["<200K", "200K-400K", "400K-600K", "600K-800K", "800K-1M", ">1M"]
    )

# House Age Group
if "house_age" in df.columns:
    df["age_group"] = pd.cut(
        df["house_age"],
        bins=[0, 10, 20, 30, 50, 75, float("inf")],
        labels=["0-10 yrs", "11-20 yrs", "21-30 yrs", "31-50 yrs", "51-75 yrs", "75+ yrs"]
    )

# ── 6. Save Cleaned Data ─────────────────────────────────────────────────────
out_path = os.path.join(DATA_DIR, "housing_cleaned.csv")
df.to_csv(out_path, index=False)
print(f"\nCleaned data saved to: {out_path}")
print(f"Final shape: {df.shape}")
