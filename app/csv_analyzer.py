import io
import pandas as pd
from fastapi import UploadFile, HTTPException

REQUIRED_COLUMNS = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]

FRAUD_THRESHOLD = 0.60


async def analyze_csv(file: UploadFile, model):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV is empty."
        )

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read CSV: {str(e)}"
        )

    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "CSV is missing required columns.",
                "missing_columns": missing
            }
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="CSV contains no transactions."
        )

    X = df[REQUIRED_COLUMNS].copy()

    try:
        probabilities = model.predict_proba(X)[:, 1]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model prediction failed: {str(e)}"
        )

    df["Fraud_Probability"] = probabilities
    df["Risk_Score"] = probabilities * 100

    df["Risk_Level"] = df["Risk_Score"].apply(
        lambda score:
            "HIGH" if score >= 70
            else "MEDIUM" if score >= 30
            else "LOW"
    )

    df["Decision"] = probabilities.apply(
        lambda probability:
            "HOLD_AND_VERIFY"
            if probability >= FRAUD_THRESHOLD
            else "APPROVE"
    ) if hasattr(probabilities, "apply") else [
        "HOLD_AND_VERIFY" if probability >= FRAUD_THRESHOLD
        else "APPROVE"
        for probability in probabilities
    ]

    high = int((df["Risk_Level"] == "HIGH").sum())
    medium = int((df["Risk_Level"] == "MEDIUM").sum())
    low = int((df["Risk_Level"] == "LOW").sum())
    alerts = int((probabilities >= FRAUD_THRESHOLD).sum())

    return {
        "filename": file.filename,
        "total_transactions": len(df),
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "fraud_alerts": alerts,
        "average_risk_score": round(
            float(df["Risk_Score"].mean()), 2
        ),
        "results": df.to_dict(orient="records")
    }
