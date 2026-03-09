"""
download_data.py
----------------
Downloads the Transformed Housing Data dataset from Kaggle
using kagglehub and copies it into the /data folder.

Prerequisites:
    1. pip install kagglehub
    2. Set up Kaggle API credentials:
       - Go to https://www.kaggle.com/settings → Account → API → Create New Token
       - This downloads kaggle.json
       - Place it at: ~/.kaggle/kaggle.json   (Linux/Mac)
                   or  C:/Users/<you>/.kaggle/kaggle.json  (Windows)
       - Run: chmod 600 ~/.kaggle/kaggle.json  (Linux/Mac only)
"""

import kagglehub
import shutil
import os

# ── 1. Download latest version of the dataset ──────────────────────────────
print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("rituparnaghosh18/transformed-housing-data-2")
print(f"Dataset downloaded to: {path}")

# ── 2. Copy files into the project /data folder ────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__))  # same folder as this script

for filename in os.listdir(path):
    src = os.path.join(path, filename)
    dst = os.path.join(DATA_DIR, filename)
    shutil.copy2(src, dst)
    print(f"  Copied: {filename}  →  data/{filename}")

print("\nAll files are ready in the /data folder.")
