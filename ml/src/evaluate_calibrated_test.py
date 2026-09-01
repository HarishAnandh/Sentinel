import joblib
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

# ==========================================
# PATHS
# ==========================================

MODEL_PATH = "ml/models/RF_DEEPER_CALIBRATED.joblib"
TEST_PATH = "data/processed/test.csv"

# ==========================================
# LOAD MODEL
# ==========================================

print("\nLoading calibrated Sentinel model...\n")

model = joblib.load(MODEL_PATH)

# ==========================================
# LOAD HOLD-OUT TEST DATA
# ==========================================

print("Loading untouched hold-out test set...\n")

df = pd.read_csv(TEST_PATH)

print(f"Test samples: {len(df):,}")
print(f"Actual fraud cases: {df['Class'].sum():,}")
print(f"Normal cases: {(df['Class'] == 0).sum():,}")

# ==========================================
# FEATURES
# ==========================================

FEATURES = [
    "Time",
    "V1", "V2", "V3", "V4", "V5",
    "V6", "V7", "V8", "V9", "V10",
    "V11", "V12", "V13", "V14", "V15",
    "V16", "V17", "V18", "V19", "V20",
    "V21", "V22", "V23", "V24", "V25",
    "V26", "V27", "V28",
    "Amount"
]

X_test = df[FEATURES]
y_test = df["Class"]

# ==========================================
# GENERATE CALIBRATED PROBABILITIES
# ==========================================

print("\nGenerating calibrated probabilities...\n")

probabilities = model.predict_proba(X_test)[:, 1]

print("Probability range:")
print(f"Minimum : {probabilities.min():.6f}")
print(f"Maximum : {probabilities.max():.6f}")

# ==========================================
# TEST MULTIPLE THRESHOLDS
# ==========================================

thresholds = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80]

print("\n==========================================")
print(" CALIBRATED MODEL — HOLD-OUT TEST")
print("==========================================")

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
    f"{'Alerts':<10}"
)

for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

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

    alerts = predictions.sum()

    print(
        f"{threshold:<12.2f}"
        f"{precision:<12.3f}"
        f"{recall:<12.3f}"
        f"{f1:<12.3f}"
        f"{alerts:<10}"
    )

# ==========================================
# FINAL PRODUCTION THRESHOLD
# ==========================================

THRESHOLD = 0.60

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
# FINAL RESULTS
# ==========================================

print("\n==========================================")
print(" FINAL CALIBRATED TEST RESULTS")
print("==========================================")

print(f"Decision threshold : {THRESHOLD:.2f}")
print(f"Precision          : {precision:.4f}")
print(f"Recall             : {recall:.4f}")
print(f"F1 Score           : {f1:.4f}")
print(f"ROC-AUC            : {roc_auc:.4f}")
print(f"PR-AUC             : {pr_auc:.4f}")

print("\n------------------------------------------")

print(f"True Negatives     : {tn:,}")
print(f"False Positives    : {fp:,}")
print(f"False Negatives    : {fn:,}")
print(f"True Positives     : {tp:,}")

print("------------------------------------------")

print(
    f"Fraud detected     : "
    f"{tp}/{tp + fn}"
)

false_alert_rate = (
    fp / (tn + fp)
) * 100

print(
    f"False alert rate   : "
    f"{false_alert_rate:.6f}%"
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions,
        digits=4
    )
)

# ==========================================
# SAVE RESULTS
# ==========================================

results = pd.DataFrame({
    "metric": [
        "threshold",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "pr_auc",
        "true_negatives",
        "false_positives",
        "false_negatives",
        "true_positives",
        "false_alert_rate"
    ],
    "value": [
        THRESHOLD,
        precision,
        recall,
        f1,
        roc_auc,
        pr_auc,
        tn,
        fp,
        fn,
        tp,
        false_alert_rate
    ]
})

OUTPUT_PATH = (
    "data/processed/"
    "calibrated_test_results.csv"
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nResults saved to:\n"
    f"{OUTPUT_PATH}"
)
