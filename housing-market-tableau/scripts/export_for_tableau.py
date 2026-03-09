"""
export_for_tableau.py
----------------------
Creates 4 focused CSV files — one per Tableau scenario — so you can
connect each sheet directly in Tableau without extra filtering.

Run from project root:
    python scripts/export_for_tableau.py
"""

import pandas as pd
import os

DATA_DIR  = os.path.join(os.path.dirname(__file__), "..", "data")
CLEAN_CSV = os.path.join(DATA_DIR, "housing_cleaned.csv")
EXPORT_DIR = os.path.join(DATA_DIR, "tableau_exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

if not os.path.exists(CLEAN_CSV):
    raise FileNotFoundError("Run scripts/data_preprocessing.py first.")

df = pd.read_csv(CLEAN_CSV)
print(f"Loaded {len(df):,} rows.\n")

# ── Scenario 1 – KPI Overview ───────────────────────────────────────────────
kpi = pd.DataFrame([{
    "total_records":    len(df),
    "avg_price":        round(df["price"].mean(), 2)         if "price" in df.columns else None,
    "total_sqft_bsmt":  int(df["sqft_basement"].sum())       if "sqft_basement" in df.columns else None,
}])
out1 = os.path.join(EXPORT_DIR, "scenario1_kpi_overview.csv")
kpi.to_csv(out1, index=False)
print(f"Scenario 1 saved  →  {out1}")

# ── Scenario 2 – Total Sales by Years Since Renovation ──────────────────────
if {"yr_since_renovation", "price_bin", "price"}.issubset(df.columns):
    scen2 = (
        df.groupby("price_bin", observed=True)
        .agg(
            total_sales=("price", "sum"),
            avg_yr_since_renovation=("yr_since_renovation", "mean"),
            house_count=("price", "count")
        )
        .reset_index()
    )
    out2 = os.path.join(EXPORT_DIR, "scenario2_sales_by_renovation.csv")
    scen2.to_csv(out2, index=False)
    print(f"Scenario 2 saved  →  {out2}")
else:
    print("Scenario 2 skipped – required columns missing.")

# ── Scenario 3 – House Age Distribution by Renovation Status ─────────────────
if {"age_group", "renovated"}.issubset(df.columns):
    scen3 = (
        df.groupby(["age_group", "renovated"], observed=True)
        .size()
        .reset_index(name="house_count")
    )
    out3 = os.path.join(EXPORT_DIR, "scenario3_age_renovation.csv")
    scen3.to_csv(out3, index=False)
    print(f"Scenario 3 saved  →  {out3}")
else:
    print("Scenario 3 skipped – required columns missing.")

# ── Scenario 4 – House Age by Bathrooms, Bedrooms, Floors ───────────────────
feature_cols = [c for c in ["bathrooms", "bedrooms", "floors"] if c in df.columns]
if "age_group" in df.columns and feature_cols:
    for feat in feature_cols:
        scen4 = (
            df.groupby(["age_group", feat], observed=True)
            .size()
            .reset_index(name="house_count")
        )
        fname = f"scenario4_age_by_{feat}.csv"
        out4 = os.path.join(EXPORT_DIR, fname)
        scen4.to_csv(out4, index=False)
        print(f"Scenario 4 ({feat}) saved  →  {out4}")
else:
    print("Scenario 4 skipped – required columns missing.")

# ── Full Cleaned Dataset (for Tableau Data Source) ───────────────────────────
full_out = os.path.join(EXPORT_DIR, "housing_full_cleaned.csv")
df.to_csv(full_out, index=False)
print(f"\nFull cleaned dataset  →  {full_out}")
print("\nAll Tableau export files are ready!")
