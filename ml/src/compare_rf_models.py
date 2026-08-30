import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score


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

print("Loading data...")

train = pd.read_csv(DATA_DIR / "train.csv")
validation = pd.read_csv(DATA_DIR / "validation.csv")

X_train = train.drop(columns=["Class"])
y_train = train["Class"]

X_val = validation.drop(columns=["Class"])
y_val = validation["Class"]


# ==========================================
# MODELS
# ==========================================

models = {

    "RF_100": RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_leaf=2,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    ),

    "RF_300": RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=2,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    ),

    "RF_DEEPER": RandomForestClassifier(
        n_estimators=200,
        max_depth=18,
        min_samples_leaf=2,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )
}


# ==========================================
# TRAIN + EVALUATE
# ==========================================

results = []

for name, model in models.items():

    print("\n==========================================")
    print(f"Training {name}")
    print("==========================================")

    model.fit(X_train, y_train)

    predictions = model.predict(X_val)

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

    results.append({
        "model": name,
        "precision": precision,
        "recall": recall,
        "f1": f1
    })

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1:        {f1:.4f}")

    model_path = MODEL_DIR / f"{name}.joblib"

    joblib.dump(model, model_path)

    print(f"Saved: {model_path}")


# ==========================================
# COMPARISON
# ==========================================

results_df = pd.DataFrame(results)

print("\n==========================================")
print("          MODEL COMPARISON")
print("==========================================")

print(
    results_df.to_string(
        index=False,
        formatters={
            "precision": "{:.4f}".format,
            "recall": "{:.4f}".format,
            "f1": "{:.4f}".format
        }
    )
)