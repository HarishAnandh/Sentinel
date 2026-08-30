from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from app.risk_engine import assess_transaction

from app.transaction_service import (
    get_fraud_transaction,
    get_normal_transaction
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Sentinel AI Risk Manager",
    description="AI-powered merchant fraud risk assessment API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# REQUEST MODEL
# ==========================================

class Transaction(BaseModel):

    Time: float

    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    Amount: float


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():

    return {
        "service": "Sentinel AI Risk Manager",
        "status": "online",
        "version": "1.0.0"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "RF_DEEPER",
        "model_loaded": True
    }


# ==========================================
# RISK ASSESSMENT
# ==========================================

@app.post("/api/v1/risk/assess")
def assess(transaction: Transaction):

    try:

        result = assess_transaction(
            transaction.model_dump()
        )

        return {
            "status": "success",
            "risk": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================
# DEMO NORMAL TRANSACTION
# ==========================================

@app.get("/api/v1/demo/normal")
def demo_normal():

    transaction = get_normal_transaction()

    risk = assess_transaction(
        transaction
    )

    return {
        "status": "success",
        "scenario": "NORMAL",
        "transaction": transaction,
        "risk": risk
    }


# ==========================================
# DEMO FRAUD TRANSACTION
# ==========================================

@app.get("/api/v1/demo/fraud")
def demo_fraud():

    transaction = get_fraud_transaction()

    risk = assess_transaction(
        transaction
    )

    return {
        "status": "success",
        "scenario": "FRAUD",
        "transaction": transaction,
        "risk": risk
    }


# ==========================================
# SERVE REACT FRONTEND
# ==========================================

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):

        requested_file = FRONTEND_DIST / full_path

        if requested_file.is_file():
            return FileResponse(requested_file)

        return FileResponse(FRONTEND_DIST / "index.html")