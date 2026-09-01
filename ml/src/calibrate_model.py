import joblib
import pandas as pd

from pathlib import Path
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# ==========================================
# PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = ROOT / "ml" / "models" / "RF_DEEPER.joblib"
VALIDATION_PATH = ROOT / "data" / "processed" / "validation.csv"

OUTPUT_MODEL = (
    ROOT
    / "ml"
    / "models"
    / "RF_DEEPER_CALIBRATED.joblib"
)

# ==========================================
# FEATURES
# ==========================================

FEATURES = [
    "Time",
    "V1", "V2", "V3", "V4",
    "V5", "V6", "V7", "V8", "V9",
    "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19",
    "V20", "V21", "V22", "V23", "V24",
    "V25", "V26", "V27", "V28",
    "Amount"
]

# ==========================================
# LOAD MODEL
# ==========================================

print("Loading RF_DEEPER...")

model = joblib.load(MODEL_PATH)

# ==========================================
# LOAD VALIDATION DATA
# ==========================================

print("Loading validation data...")

df = pd.read_csv(VALIDATION_PATH)

X = df[FEATURES]
y = df["Class"]

print(f"Validation samples: {len(df)}")
print(f"Fraud cases: {y.sum()}")
print(f"Normal cases: {(y == 0).sum()}")

# ==========================================
# ORIGINAL MODEL
# ==========================================

print("\nGenerating original probabilities...")

original_probabilities = model.predict_proba(X)[:, 1]

# ==========================================
# CALIBRATION
# ==========================================

print("\nCalibrating model...")

calibrated_model = CalibratedClassifierCV(
    model,
    method="sigmoid",
    cv="prefit"
)

calibrated_model.fit(X, y)

# ==========================================
# CALIBRATED PROBABILITIES
# ==========================================

print("Generating calibrated probabilities...")

calibrated_probabilities = (
    calibrated_model.predict_proba(X)[:, 1]
)

# ==========================================
# COMPARE PROBABILITY RANGES
# ==========================================

print("\n==========================================")
print("PROBABILITY COMPARISON")
print("==========================================")

print(
    f"Original min : {original_probabilities.min():.6f}"
)

print(
    f"Original max : {original_probabilities.max():.6f}"
)

print(
    f"Calibrated min : {calibrated_probabilities.min():.6f}"
)

print(
    f"Calibrated max : {calibrated_probabilities.max():.6f}"
)

# ==========================================
# THRESHOLD TEST
# ==========================================

print("\n==========================================")
print("CALIBRATED THRESHOLD ANALYSIS")
print("==========================================")

for threshold in [0.30, 0.40, 0.50, 0.60, 0.70]:

    predictions = (
        calibrated_probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y,
        predictions,
        zero_division=0
    )

    print(
        f"Threshold {threshold:.2f} | "
        f"Precision {precision:.3f} | "
        f"Recall {recall:.3f} | "
        f"F1 {f1:.3f}"
    )

# ==========================================
# ROC-AUC
# ==========================================

auc = roc_auc_score(
    y,
    calibrated_probabilities
)

print(
    f"\nCalibrated ROC-AUC: {auc:.4f}"
)

# ==========================================
# SAVE
# ==========================================

joblib.dump(
    calibrated_model,
    OUTPUT_MODEL
)

print("\n==========================================")
print("CALIBRATED MODEL SAVED")
print("==========================================")

print(OUTPUT_MODEL)
