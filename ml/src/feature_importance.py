import pandas as pd
import joblib

from pathlib import Path


# ==========================================
# PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data" / "processed"
MODEL_PATH = ROOT / "ml" / "models" / "sentinel_random_forest.joblib"


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading Sentinel Random Forest...")

model = joblib.load(MODEL_PATH)


# ==========================================
# LOAD FEATURE NAMES
# ==========================================

train = pd.read_csv(
    DATA_DIR / "train.csv",
    nrows=1
)

feature_names = train.drop(
    columns=["Class"]
).columns


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importance
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)


# ==========================================
# DISPLAY
# ==========================================

print("\n==========================================")
print("       SENTINEL FEATURE IMPORTANCE")
print("==========================================\n")

print(
    importance_df.to_string(
        index=False,
        formatters={
            "importance": "{:.6f}".format
        }
    )
)


# ==========================================
# SAVE
# ==========================================

output_path = DATA_DIR / "feature_importance.csv"

importance_df.to_csv(
    output_path,
    index=False
)

print(
    f"\nSaved to:\n{output_path}"
)