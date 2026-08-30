import pandas as pd
import joblib

from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
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


# ==========================================
# FEATURES / TARGET
# ==========================================

X_train = train.drop(columns=["Class"])
y_train = train["Class"]

X_val = validation.drop(columns=["Class"])
y_val = validation["Class"]


print(f"\nTraining samples: {len(X_train):,}")
print(f"Validation samples: {len(X_val):,}")

print(f"Training fraud cases: {y_train.sum():,}")
print(f"Validation fraud cases: {y_val.sum():,}")


# ==========================================
# MODEL
# ==========================================

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        )
    )
])


# ==========================================
# TRAIN
# ==========================================

print("\nTraining Logistic Regression...")

model.fit(X_train, y_train)

print("Training complete.")


# ==========================================
# VALIDATION PREDICTION
# ==========================================

y_pred = model.predict(X_val)


# ==========================================
# METRICS
# ==========================================

precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)

cm = confusion_matrix(y_val, y_pred)


print("\n==========================================")
print("       SENTINEL BASELINE RESULTS")
print("==========================================")

print(f"\nPrecision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_val, y_pred))


# ==========================================
# SAVE MODEL
# ==========================================

model_path = MODEL_DIR / "baseline_logistic_regression.joblib"

joblib.dump(model, model_path)

print(f"\nModel saved to:")
print(model_path)