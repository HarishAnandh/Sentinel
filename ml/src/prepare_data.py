import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


# ==============================
# PATHS
# ==============================

ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = ROOT / "data" / "raw" / "creditcard.csv"
PROCESSED_DIR = ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# LOAD DATA
# ==============================

print("Loading dataset...")

df = pd.read_csv(RAW_DATA)

print(f"Dataset loaded: {df.shape}")


# ==============================
# SEPARATE FEATURES AND TARGET
# ==============================

X = df.drop(columns=["Class"])
y = df["Class"]


# ==============================
# FIRST SPLIT
# ==============================

# 80% development data
# 20% completely untouched test data

X_dev, X_test, y_dev, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)


# ==============================
# SECOND SPLIT
# ==============================

# Split development data into:
# 70% training
# 10% validation

X_train, X_val, y_train, y_val = train_test_split(
    X_dev,
    y_dev,
    test_size=0.125,
    stratify=y_dev,
    random_state=42
)


# ==============================
# SAVE SPLITS
# ==============================

train = X_train.copy()
train["Class"] = y_train

validation = X_val.copy()
validation["Class"] = y_val

test = X_test.copy()
test["Class"] = y_test


train.to_csv(PROCESSED_DIR / "train.csv", index=False)
validation.to_csv(PROCESSED_DIR / "validation.csv", index=False)
test.to_csv(PROCESSED_DIR / "test.csv", index=False)


# ==============================
# REPORT
# ==============================

print("\n========== SPLIT SUMMARY ==========")

print(f"Training:   {train.shape}")
print(f"Validation: {validation.shape}")
print(f"Test:       {test.shape}")

print("\n========== CLASS DISTRIBUTION ==========")

print("\nTraining:")
print(y_train.value_counts())

print("\nValidation:")
print(y_val.value_counts())

print("\nTest:")
print(y_test.value_counts())

print("\nData preparation complete.")