import joblib
import pandas as pd

from pathlib import Path


# ==========================================
# PATH CONFIGURATION
# ==========================================

ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    ROOT
    / "ml"
    / "models"
    / "RF_DEEPER_CALIBRATED.joblib"
)


# ==========================================
# LOAD MODEL ONCE
# ==========================================

print("Loading Sentinel risk model...")

model = joblib.load(MODEL_PATH)


# ==========================================
# MODEL FEATURES
# ==========================================

FEATURES = [
    "Time",
    "V1",
    "V2",
    "V3",
    "V4",
    "V5",
    "V6",
    "V7",
    "V8",
    "V9",
    "V10",
    "V11",
    "V12",
    "V13",
    "V14",
    "V15",
    "V16",
    "V17",
    "V18",
    "V19",
    "V20",
    "V21",
    "V22",
    "V23",
    "V24",
    "V25",
    "V26",
    "V27",
    "V28",
    "Amount"
]

# ==========================================
# PRODUCTION RISK THRESHOLD
# ==========================================

FRAUD_THRESHOLD = 0.60
# ==========================================
# RISK LEVEL
# ==========================================

def get_risk_level(risk_score):

    if risk_score < 30:
        return "LOW"

    elif risk_score < 70:
        return "MEDIUM"

    else:
        return "HIGH"


# ==========================================
# MERCHANT ACTION
# ==========================================

FRAUD_THRESHOLD = 0.60


def get_action(fraud_probability):
    if fraud_probability >= FRAUD_THRESHOLD:
        return "HOLD_AND_VERIFY"
    elif fraud_probability >= 0.30:
        return "REVIEW"
    else:
        return "APPROVE"


# ==========================================
# MAIN RISK FUNCTION
# ==========================================

def assess_transaction(transaction):

    # --------------------------------------
    # Create dataframe
    # --------------------------------------

    data = {}

    for feature in FEATURES:

        if feature not in transaction:
            raise ValueError(
                f"Missing feature: {feature}"
            )

        data[feature] = transaction[feature]

    df = pd.DataFrame(
        [data],
        columns=FEATURES
    )


    # --------------------------------------
    # Fraud probability
    # --------------------------------------

    fraud_probability = model.predict_proba(
        df
    )[0][1]


    # --------------------------------------
    # Convert to 0-100
    # --------------------------------------

    risk_score = round(
        fraud_probability * 100,
        2
    )


    # --------------------------------------
    # Risk classification
    # --------------------------------------

    risk_level = get_risk_level(
        risk_score
    )


    # --------------------------------------
    # Merchant decision
    # --------------------------------------

    action = get_action(
        fraud_probability
    )


        # --------------------------------------
    # Model-level feature importance
    # --------------------------------------

    # CalibratedClassifierCV wraps the original
# Random Forest model inside calibrated_classifiers_

    base_model = model.calibrated_classifiers_[0].estimator

    feature_importance = dict(
        zip(
            FEATURES,
            base_model.feature_importances_
        )
    )

    top_features = sorted(
        feature_importance.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    model_signals = [
        {
            "feature": feature,
            "importance": round(
                float(importance),
                4
            )
        }
        for feature, importance in top_features
    ]

    # --------------------------------------
    # Return result
    # --------------------------------------
        # --------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------

    feature_importance = {
        "V14": 0.183251,
        "V10": 0.114612,
        "V4": 0.114152,
        "V12": 0.098673,
        "V17": 0.089387,
        "V3": 0.060574,
        "V16": 0.055694,
        "V11": 0.052602,
        "V2": 0.032596,
        "V7": 0.022523
    }

    top_features = sorted(
        feature_importance.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    signals = []

    for feature, importance in top_features:
        value = transaction[feature]

        if abs(value) >= 3:
            severity = "Strong signal"
        elif abs(value) >= 1.5:
            severity = "Significant"
        else:
            severity = "Moderate"

        signals.append({
            "feature": feature,
            "value": round(float(value), 4),
            "importance": round(importance, 4),
            "impact": round(importance * 100, 1),
            "severity": severity
        })

    # --------------------------------------
    # Return result
    # --------------------------------------

    return {
        "risk_score": risk_score,
        "risk_probability": round(
            fraud_probability,
            4
        ),
        "risk_level": risk_level,
        "decision": action,
        "signals": signals
    }


# ==========================================
# LOCAL TEST
# ==========================================

if __name__ == "__main__":

    print("\nTesting Sentinel Risk Engine...\n")

    sample_transaction = {
        "Time": 406.0,

        "V1": -2.3122265423263,
        "V2": 1.95199201064158,
        "V3": -1.60985073229769,
        "V4": 3.9979055875468,
        "V5": -0.52218786466776,
        "V6": -1.42654531990165,
        "V7": -2.537387306245,
        "V8": 1.39165724829804,
        "V9": -2.77008927719433,
        "V10": -2.77227214465915,
        "V11": 3.202033207096,
        "V12": -2.899907388494,
        "V13": -0.595221881324,
        "V14": -4.289253782442,
        "V15": 0.389724120274,
        "V16": -1.140747179609,
        "V17": -2.830055674991,
        "V18": -0.016822468,
        "V19": 0.416955705037,
        "V20": 0.126910559,
        "V21": 0.517232370092,
        "V22": -0.035049369877,
        "V23": -0.465211076182,
        "V24": 0.320198198514,
        "V25": 0.044519167473,
        "V26": 0.177839798284,
        "V27": 0.261145002567,
        "V28": -0.143275874698,

        "Amount": 0
    }


    result = assess_transaction(
        sample_transaction
    )


    print("==========================================")
    print("       SENTINEL RISK ASSESSMENT")
    print("==========================================")

    print(
        f"\nRisk score       : "
        f"{result['risk_score']}/100"
    )

    print(
        f"Risk probability : "
        f"{result['risk_probability']}"
    )

    print(
        f"Risk level       : "
        f"{result['risk_level']}"
    )

    print(
        f"Decision          : "
        f"{result['decision']}"
    )