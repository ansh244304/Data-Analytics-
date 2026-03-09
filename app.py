from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import os, json

import kagglehub
path = kagglehub.dataset_download("rituparnaghosh18/transformed-housing-data-2")
print("Dataset path:", path)

app = Flask(__name__)

# ── Load & clean data ─────────────────────────────────────
def load_data():
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(path, csv_files[0]))
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    return df

df = load_data()
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

def safe_json(obj):
    return json.loads(json.dumps(obj, default=str))

# ── Helper: pick column by keyword ───────────────────────
def col(keywords):
    for k in keywords:
        found = next((c for c in df.columns if k in c), None)
        if found: return found
    return None

price_col   = col(['price'])
area_col    = col(['area', 'size', 'sqft'])
bed_col     = col(['bed', 'bhk', 'room'])
loc_col     = col(['location', 'city', 'area', 'region'])
cat_col     = next((c for c in df.columns if df[c].dtype == 'object'), None)
date_col    = col(['date', 'year'])

# ── Routes ────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/kpis')
def kpis():
    num_df = df.select_dtypes(include='number')
    avg_p  = round(df[price_col].mean(), 0) if price_col else 0
    med_p  = round(df[price_col].median(), 0) if price_col else 0
    return jsonify({
        "total":    len(df),
        "columns":  len(df.columns),
        "missing":  int(df.isnull().sum().sum()),
        "avg_price": avg_p,
        "med_price": med_p,
        "numeric":  len(num_df.columns)
    })

@app.route('/api/price_dist')
def price_dist():
    if not price_col: return jsonify({"error": "no price col"})
    bins   = pd.cut(df[price_col].dropna(), bins=12)
    counts = bins.value_counts().sort_index()
    return jsonify({"labels": [str(i) for i in counts.index], "values": counts.values.tolist()})

@app.route('/api/avg_by_cat')
def avg_by_cat():
    if not price_col or not cat_col: return jsonify({"error": "cols missing"})
    grp = df.groupby(cat_col)[price_col].mean().sort_values(ascending=False).head(8)
    return jsonify({"labels": grp.index.tolist(), "values": [round(v,2) for v in grp.values]})

@app.route('/api/bedrooms')
def bedrooms():
    if not bed_col: return jsonify({"error": "no bed col"})
    counts = df[bed_col].value_counts().sort_index().head(8)
    return jsonify({"labels": [str(k) for k in counts.index], "values": counts.values.tolist()})

@app.route('/api/scatter')
def scatter():
    if not price_col or not area_col: return jsonify({"error": "cols missing"})
    s = df[[area_col, price_col]].dropna().sample(min(400, len(df)), random_state=42)
    return jsonify({"x": s[area_col].tolist(), "y": s[price_col].tolist()})

@app.route('/api/top_locations')
def top_locations():
    if not price_col or not loc_col: return jsonify({"error": "cols missing"})
    grp = df.groupby(loc_col)[price_col].mean().sort_values(ascending=False).head(8)
    return jsonify({"labels": grp.index.tolist(), "values": [round(v,2) for v in grp.values]})

@app.route('/api/trend')
def trend():
    if not price_col: return jsonify({"error": "no price col"})
    if date_col:
        grp = df.groupby(date_col)[price_col].mean()
        return jsonify({"labels": grp.index.astype(str).tolist(), "values": [round(v,2) for v in grp.values]})
    rolling = df[price_col].dropna().rolling(50).mean().dropna()
    step    = max(1, len(rolling) // 40)
    return jsonify({"labels": list(range(0, len(rolling), step)),
                    "values": [round(v,2) for v in rolling.iloc[::step]]})

@app.route('/api/table')
def table():
    s = df.head(100).fillna('N/A')
    return jsonify({"columns": df.columns.tolist(), "rows": safe_json(s.values.tolist())})

if __name__ == '__main__':
    app.run(debug=True)
