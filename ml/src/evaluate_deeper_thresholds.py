import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ==========================================
# PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data" / "processed"
MODEL_PATH = ROOT / "ml" / "models" / "RF_DEEPER.joblib"


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading RF_DEEPER model...")

model = joblib.load(MODEL_PATH)


# ==========================================
# LOAD VALIDATION DATA
# ==========================================

print("Loading validation data...")

validation = pd.read_csv(
    DATA_DIR / "validation.csv"
)

X_val = validation.drop(columns=["Class"])
y_val = validation["Class"]


# ==========================================
# GENERATE PROBABILITIES
# ==========================================

print("Generating fraud probabilities...")

probabilities = model.predict_proba(X_val)[:, 1]


# ==========================================
# THRESHOLDS
# ==========================================

thresholds = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]


# ==========================================
# TEMPORARY BUSINESS COSTS
# ==========================================

FALSE_POSITIVE_COST = 100
FALSE_NEGATIVE_COST = 2500


# ==========================================
# EVALUATION
# ==========================================

results = []


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_val,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_val,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_val,
        predictions,
        zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(
        y_val,
        predictions
    ).ravel()

    fp_cost = fp * FALSE_POSITIVE_COST
    fn_cost = fn * FALSE_NEGATIVE_COST

    total_cost = fp_cost + fn_cost

    results.append({
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "alerts": tp + fp,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "fp_cost": fp_cost,
        "fn_cost": fn_cost,
        "total_cost": total_cost
    })


# ==========================================
# DISPLAY
# ==========================================

results_df = pd.DataFrame(results)

print("\n==========================================")
print("       RF_DEEPER THRESHOLD ANALYSIS")
print("==========================================\n")

print(
    results_df.to_string(
        index=False,
        formatters={
            "precision": "{:.3f}".format,
            "recall": "{:.3f}".format,
            "f1": "{:.3f}".format
        }
    )
)


# ==========================================
# BEST BY COST
# ==========================================

best_cost = results_df.loc[
    results_df["total_cost"].idxmin()
]


print("\n==========================================")
print("        BEST THRESHOLD BY COST")
print("==========================================")

print(
    f"\nThreshold: {best_cost['threshold']:.2f}"
)

print(
    f"Precision: {best_cost['precision']:.3f}"
)

print(
    f"Recall: {best_cost['recall']:.3f}"
)

print(
    f"F1: {best_cost['f1']:.3f}"
)

print(
    f"Alerts: {int(best_cost['alerts'])}"
)

print(
    f"True positives: {int(best_cost['true_positives'])}"
)

print(
    f"False positives: {int(best_cost['false_positives'])}"
)

print(
    f"False negatives: {int(best_cost['false_negatives'])}"
)

print(
    f"Estimated total cost: ₹{best_cost['total_cost']:,.0f}"
)


# ==========================================
# SAVE
# ==========================================

output_path = DATA_DIR / "deeper_threshold_results.csv"

results_df.to_csv(
    output_path,
    index=False
)

print(
    f"\nResults saved to:\n{output_path}"
)