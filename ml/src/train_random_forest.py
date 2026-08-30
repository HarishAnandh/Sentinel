import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data" / "processed"
MODEL_DIR = ROOT / "ml" / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# LOAD DATA
# ==========================================

print("Loading datasets...")

train = pd.read_csv(DATA_DIR / "train.csv")
validation = pd.read_csv(DATA_DIR / "validation.csv")


X_train = train.drop(columns=["Class"])
y_train = train["Class"]

X_val = validation.drop(columns=["Class"])
y_val = validation["Class"]


print(f"\nTraining samples: {len(X_train):,}")
print(f"Validation samples: {len(X_val):,}")

print(f"Training fraud cases: {y_train.sum():,}")
print(f"Validation fraud cases: {y_val.sum():,}")


# ==========================================
# RANDOM FOREST
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=2,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42
)


# ==========================================
# TRAIN
# ==========================================

print("\nTraining Random Forest...")

model.fit(X_train, y_train)

print("Training complete.")


# ==========================================
# VALIDATION PREDICTIONS
# ==========================================

y_pred = model.predict(X_val)


# ==========================================
# METRICS
# ==========================================

precision = precision_score(
    y_val,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_val,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_val,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(
    y_val,
    y_pred
)


# ==========================================
# RESULTS
# ==========================================

print("\n==========================================")
print("       RANDOM FOREST RESULTS")
print("==========================================")

print(f"\nPrecision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(
    classification_report(
        y_val,
        y_pred,
        zero_division=0
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

model_path = MODEL_DIR / "sentinel_random_forest.joblib"

joblib.dump(
    model,
    model_path
)

print(f"\nModel saved to:")
print(model_path)