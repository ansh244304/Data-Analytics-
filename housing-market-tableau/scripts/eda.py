"""
eda.py
------
Exploratory Data Analysis — generates summary stats and charts
that mirror the 4 Tableau scenarios.

Run from project root:
    python scripts/eda.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Config ──────────────────────────────────────────────────────────────────
DATA_DIR  = os.path.join(os.path.dirname(__file__), "..", "data")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "..", "data", "eda_charts")
os.makedirs(OUT_DIR, exist_ok=True)

CLEAN_CSV = os.path.join(DATA_DIR, "housing_cleaned.csv")
if not os.path.exists(CLEAN_CSV):
    raise FileNotFoundError("Run scripts/data_preprocessing.py first.")

df = pd.read_csv(CLEAN_CSV)
print(f"Loaded {len(df):,} rows, {df.shape[1]} columns.\n")

sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 120})

# ── Scenario 1 – KPI Overview ───────────────────────────────────────────────
print("=" * 50)
print("SCENARIO 1 — Overall Data Overview")
print("=" * 50)
total_records = len(df)
avg_price     = df["price"].mean()             if "price"         in df.columns else "N/A"
total_sqft    = df["sqft_basement"].sum()      if "sqft_basement"  in df.columns else "N/A"

print(f"  Total Records          : {total_records:,}")
print(f"  Average Sale Price     : ${avg_price:,.2f}" if isinstance(avg_price, float) else f"  Average Sale Price     : {avg_price}")
print(f"  Total Basement Sqft    : {total_sqft:,.0f}" if isinstance(total_sqft, float) else f"  Total Basement Sqft    : {total_sqft}")

# ── Scenario 2 – Sales by Years Since Renovation ────────────────────────────
if "yr_since_renovation" in df.columns and "price_bin" in df.columns:
    print("\n" + "=" * 50)
    print("SCENARIO 2 — Total Sales by Years Since Renovation")
    print("=" * 50)

    grp = (
        df.groupby("price_bin", observed=True)["yr_since_renovation"]
        .sum()
        .reset_index()
        .rename(columns={"yr_since_renovation": "total_yrs"})
    )
    print(grp.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=grp, x="price_bin", y="total_yrs", palette="Blues_r", ax=ax)
    ax.set_title("Scenario 2 — Total Sales by Years Since Renovation", fontsize=14, fontweight="bold")
    ax.set_xlabel("Sale Price Bin")
    ax.set_ylabel("Total Years Since Renovation")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "scenario2_sales_by_renovation.png"))
    plt.close()
    print("  Chart saved.")

# ── Scenario 3 – House Age by Renovation Status ─────────────────────────────
if "age_group" in df.columns and "renovated" in df.columns:
    print("\n" + "=" * 50)
    print("SCENARIO 3 — House Age Distribution by Renovation Status")
    print("=" * 50)

    pie_data = df["age_group"].value_counts(sort=False)
    print(pie_data.to_string())

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = sns.color_palette("Blues", n_colors=len(pie_data))
    ax.pie(
        pie_data,
        labels=pie_data.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
    )
    ax.set_title("Scenario 3 — House Age Distribution by Renovation Status", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "scenario3_age_renovation_pie.png"))
    plt.close()
    print("  Chart saved.")

# ── Scenario 4 – House Age by Bathrooms, Bedrooms, Floors ──────────────────
feature_cols = [c for c in ["bathrooms", "bedrooms", "floors"] if c in df.columns]
if "age_group" in df.columns and feature_cols:
    print("\n" + "=" * 50)
    print("SCENARIO 4 — House Age Distribution by Features")
    print("=" * 50)

    fig, axes = plt.subplots(1, len(feature_cols), figsize=(6 * len(feature_cols), 6))
    if len(feature_cols) == 1:
        axes = [axes]

    for ax, feat in zip(axes, feature_cols):
        grp4 = df.groupby(["age_group", feat], observed=True).size().reset_index(name="count")
        # Keep top 5 values of the feature to keep chart readable
        top_vals = df[feat].value_counts().head(5).index.tolist()
        grp4 = grp4[grp4[feat].isin(top_vals)]
        sns.barplot(data=grp4, x="age_group", y="count", hue=feat, palette="Blues", ax=ax)
        ax.set_title(f"Age Group vs {feat.capitalize()}", fontsize=12, fontweight="bold")
        ax.set_xlabel("House Age Group")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=30)
        ax.legend(title=feat.capitalize(), loc="upper right", fontsize=8)

    fig.suptitle("Scenario 4 — House Age Distribution by Features", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "scenario4_age_by_features.png"))
    plt.close()
    print("  Chart saved.")

print(f"\nAll EDA charts saved to: {OUT_DIR}")
