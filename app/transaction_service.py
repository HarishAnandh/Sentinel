import pandas as pd

from pathlib import Path


# ==========================================
# PATH
# ==========================================

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "test.csv"
)


# ==========================================
# LOAD TEST DATA
# ==========================================

print("Loading transaction dataset...")

transactions = pd.read_csv(
    DATA_PATH
)


# ==========================================
# REMOVE LABEL
# ==========================================

FEATURES = [
    column
    for column in transactions.columns
    if column != "Class"
]


# ==========================================
# GET TRANSACTION
# ==========================================

def get_transaction(index=None):

    if index is None:

        row = transactions.sample(
            1
        ).iloc[0]

    else:

        row = transactions.iloc[
            index
        ]


    transaction = {}

    for feature in FEATURES:

        transaction[feature] = float(
            row[feature]
        )


    return transaction


# ==========================================
# GET KNOWN FRAUD
# ==========================================

def get_fraud_transaction():

    fraud = transactions[
        transactions["Class"] == 1
    ]

    row = fraud.sample(
        1
    ).iloc[0]


    transaction = {}

    for feature in FEATURES:

        transaction[feature] = float(
            row[feature]
        )


    return transaction


# ==========================================
# GET KNOWN NORMAL
# ==========================================

def get_normal_transaction():

    normal = transactions[
        transactions["Class"] == 0
    ]

    row = normal.sample(
        1
    ).iloc[0]


    transaction = {}

    for feature in FEATURES:

        transaction[feature] = float(
            row[feature]
        )


    return transaction