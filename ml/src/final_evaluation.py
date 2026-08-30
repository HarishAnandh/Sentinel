import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    average_precision_score
)


# ==========================================
# PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data" / "processed"
MODEL_PATH = ROOT / "ml" / "models" / "RF_DEEPER.joblib"


# ==========================================
# CONFIGURATION
# ==========================================

THRESHOLD = 0.50


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading final Sentinel model...")

model = joblib.load(MODEL_PATH)


# ==========================================
# LOAD TEST DATA
# ==========================================

print("Loading HOLD-OUT TEST SET...")

test = pd.read_csv(
    DATA_DIR / "test.csv"
)

X_test = test.drop(
    columns=["Class"]
)

y_test = test["Class"]


print(f"\nTest samples: {len(test):,}")
print(f"Actual fraud cases: {y_test.sum():,}")


# ==========================================
# GENERATE PROBABILITIES
# ==========================================

print("\nGenerating predictions...")

probabilities = model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# APPLY LOCKED THRESHOLD
# ==========================================

predictions = (
    probabilities >= THRESHOLD
).astype(int)


# ==========================================
# METRICS
# ==========================================

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)

pr_auc = average_precision_score(
    y_test,
    probabilities
)

tn, fp, fn, tp = confusion_matrix(
    y_test,
    predictions
).ravel()


# ==========================================
# RESULTS
# ==========================================

print("\n==========================================")
print("       SENTINEL FINAL TEST RESULTS")
print("==========================================")

print(f"\nDecision threshold : {THRESHOLD:.2f}")

print(f"\nPrecision          : {precision:.4f}")
print(f"Recall             : {recall:.4f}")
print(f"F1 Score           : {f1:.4f}")
print(f"ROC-AUC            : {roc_auc:.4f}")
print(f"PR-AUC             : {pr_auc:.4f}")

print("\n------------------------------------------")

print(f"True Negatives     : {tn}")
print(f"False Positives    : {fp}")
print(f"False Negatives    : {fn}")
print(f"True Positives     : {tp}")

print("------------------------------------------")

print(
    f"\nFraud detected: {tp}/{tp + fn}"
)

print(
    f"False alert rate: "
    f"{fp / (fp + tn):.6%}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ==========================================
# SAVE OFFICIAL RESULTS
# ==========================================

results = pd.DataFrame([{
    "model": "RF_DEEPER",
    "threshold": THRESHOLD,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "roc_auc": roc_auc,
    "pr_auc": pr_auc,
    "true_negatives": tn,
    "false_positives": fp,
    "false_negatives": fn,
    "true_positives": tp
}])


output_path = DATA_DIR / "final_test_results.csv"

results.to_csv(
    output_path,
    index=False
)


print(
    f"\nOfficial results saved to:\n{output_path}"
)