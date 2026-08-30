import pandas as pd
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATA_PATH = ROOT / "data" / "raw" / "creditcard.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum().sum())

print("\n========== CLASS DISTRIBUTION ==========")
print(df["Class"].value_counts())

print("\n========== CLASS PERCENTAGE ==========")
print(df["Class"].value_counts(normalize=True) * 100)

print("\n========== AMOUNT STATISTICS ==========")
print(df["Amount"].describe())


import matplotlib.pyplot as plt

class_counts = df["Class"].value_counts()

plt.figure(figsize=(8, 5))
class_counts.plot(kind="bar")

plt.title("Transaction Class Distribution")
plt.xlabel("Class (0 = Legitimate, 1 = Fraud)")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()