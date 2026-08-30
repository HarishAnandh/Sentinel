# 🛡️ Sentinel AI Risk Manager

## AI-Powered Transaction Fraud Risk Assessment & Merchant Decision Support

Sentinel is an AI-powered transaction risk management platform designed to help merchants identify potentially fraudulent transactions and make informed decisions before processing them.

Unlike a traditional binary fraud detector that simply returns:

    Fraud / Not Fraud

Sentinel converts machine-learning predictions into an actionable risk assessment containing:

- Risk probability
- Risk score
- Risk level
- Recommended merchant decision
- Important risk signals
- Feature-level impact information

The goal is to bridge the gap between a machine-learning prediction and a practical merchant decision.

---

# 📌 Table of Contents

1. [Problem Statement](#-problem-statement)
2. [Solution](#-solution)
3. [How Sentinel Works](#-how-sentinel-works)
4. [Current Functionality](#-current-functionality)
5. [Machine Learning Pipeline](#-machine-learning-pipeline)
6. [Risk Assessment System](#-risk-assessment-system)
7. [Explainable Risk Signals](#-explainable-risk-signals)
8. [System Architecture](#-system-architecture)
9. [Project Structure](#-project-structure)
10. [Technology Stack](#-technology-stack)
11. [Backend API](#-backend-api)
12. [Frontend](#-frontend)
13. [Dataset](#-dataset)
14. [Machine Learning Models](#-machine-learning-models)
15. [Model Evaluation](#-model-evaluation)
16. [Local Setup](#-local-setup)
17. [Running the Backend](#-running-the-backend)
18. [Running the Frontend](#-running-the-frontend)
19. [Testing the API](#-testing-the-api)
20. [Deployment](#-deployment)
21. [Deployment Problems & Solutions](#-deployment-problems--solutions)
22. [Git Repository Setup](#-git-repository-setup)
23. [Current Deployment](#-current-deployment)
24. [Future Enhancements](#-future-enhancements)
25. [Project Vision](#-project-vision)

---

# 🎯 Problem Statement

Online transaction fraud is a major challenge for merchants and financial platforms.

A fraud detection model can identify suspicious transactions, but a raw prediction is not always sufficient for operational decision-making.

For example:

    Fraud Probability = 0.91

does not directly tell a merchant what to do.

Should the transaction be:

- Approved?
- Reviewed?
- Temporarily held?
- Verified with the customer?

Sentinel addresses this problem by converting machine-learning predictions into a structured risk management workflow.

---

# 💡 Solution

Sentinel analyzes transaction characteristics using a trained Random Forest model and converts the prediction into a merchant-friendly risk assessment.

The system provides:

    Transaction
        ↓
    Machine Learning Model
        ↓
    Fraud Probability
        ↓
    Risk Score
        ↓
    Risk Level
        ↓
    Recommended Decision
        ↓
    Explainable Risk Signals

This makes the system more useful than a simple binary classifier.

---

# ⚙️ How Sentinel Works

The current system follows this pipeline:

    Transaction Data
           │
           ▼
    ┌─────────────────┐
    │   FastAPI API   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   Risk Engine   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ RF_DEEPER Model │
    └────────┬────────┘
             │
             ▼
    Fraud Probability
             │
             ▼
       Risk Score
             │
       ┌─────┴─────┐
       ▼           ▼
    Risk Level   Decision
       │           │
       └─────┬─────┘
             ▼
    Explainable Signals
             │
             ▼
      React Dashboard

---

# 🚀 Current Functionality

The current deployed Sentinel system supports:

## 1. Transaction Risk Assessment

The backend accepts transaction attributes including:

- Time
- V1–V28
- Amount

These features are passed to the trained machine-learning model.

---

## 2. Fraud Probability

The model produces a probability representing the estimated fraud risk.

Example:

    Risk Probability: 0.9999

---

## 3. Risk Score

The probability is converted into a user-friendly risk score.

Example:

    Risk Score: 99.99 / 100

---

## 4. Risk Classification

The system converts the prediction into a risk category.

Example:

    HIGH

---

## 5. Merchant Decision

Sentinel converts the risk classification into an actionable decision.

Example:

    HIGH RISK
        ↓
    HOLD_AND_VERIFY

This allows the system to provide an operational recommendation rather than only a prediction.

---

## 6. Explainable Risk Signals

The system identifies important features contributing to the risk prediction.

Example:

    V14 → 18.3% impact → Strong signal
    V10 → 11.5% impact → Significant
    V4  → 11.4% impact → Strong signal
    V12 → 9.9% impact  → Strong signal
    V17 → 8.9% impact  → Strong signal

This provides additional context behind the model prediction.

---

## 7. Demo Transactions

The backend currently provides two demonstration scenarios:

    Normal Transaction

and

    Fraud Transaction

These allow the deployed application to demonstrate the model without manually entering all model features.

---

# 🧠 Machine Learning Pipeline

The machine-learning component was developed separately from the application layer.

The general workflow is:

    Raw Dataset
         ↓
    Data Preparation
         ↓
    Train / Validation / Test Split
         ↓
    Exploratory Data Analysis
         ↓
    Baseline Model
         ↓
    Random Forest Models
         ↓
    Model Comparison
         ↓
    Feature Importance
         ↓
    Threshold Evaluation
         ↓
    Final Model
         ↓
    Deployment

---

# 📊 Dataset

The project uses transaction data containing anonymized numerical features.

The main transaction attributes include:

    Time
    V1
    V2
    ...
    V28
    Amount

The raw dataset was used during machine-learning development and training.

Because the raw dataset is large, it is intentionally excluded from the final Git repository.

The `.gitignore` contains:

    data/raw/

This prevents the original large training dataset from being committed again.

---

# 🤖 Machine Learning Models

Several models were developed and evaluated during the project.

The repository currently contains:

    ml/models/

        RF_100.joblib
        RF_300.joblib
        RF_DEEPER.joblib
        baseline_logistic_regression.joblib
        sentinel_random_forest.joblib

The deeper Random Forest model used by the deployed risk engine is:

    RF_DEEPER.joblib

---

# 🔬 Model Development Scripts

The `ml/src/` directory contains the machine-learning development pipeline.

Important scripts include:

    prepare_data.py
        Data preparation

    eda.py
        Exploratory data analysis

    train_baseline.py
        Baseline model training

    train_random_forest.py
        Random Forest training

    compare_rf_models.py
        Comparison of Random Forest configurations

    feature_importance.py
        Feature importance analysis

    evaluate_thresholds.py
        Threshold evaluation

    evaluate_rf_thresholds.py
        Random Forest threshold evaluation

    evaluate_deeper_thresholds.py
        Deeper model threshold evaluation

    final_evaluation.py
        Final model evaluation

---

# 📈 Model Evaluation

Model development was not limited to training a single classifier.

Different Random Forest configurations were evaluated before selecting the model used by the application.

The repository contains evaluation outputs including:

    data/processed/

        feature_importance.csv
        threshold_results.csv
        rf_threshold_results.csv
        deeper_threshold_results.csv
        final_test_results.csv

These files document the model evaluation process.

---

# 🔍 Explainability

A major design goal of Sentinel is to provide more information than a simple prediction.

Instead of:

    Fraud = TRUE

the system returns information such as:

    Risk Score: 99.99

    Risk Level: HIGH

    Decision: HOLD_AND_VERIFY

    Important Signals:
        V14
        V10
        V4
        V12
        V17

This makes the output easier for a merchant or evaluator to understand.

---

# 🏗️ System Architecture

The current architecture consists of three major layers.

## 1. Frontend

    React
       ↓
    Merchant Dashboard

The frontend provides the user interface for interacting with Sentinel.

---

## 2. Backend

    FastAPI
       ↓
    Risk Engine
       ↓
    Machine Learning Model

The backend performs transaction assessment and exposes REST APIs.

---

## 3. Machine Learning

    RF_DEEPER.joblib

The trained Random Forest model performs the fraud-risk prediction.

---

# 📁 Project Structure

```text
Sentinel/
│
├── app/
│   ├── main.py
│   ├── risk_engine.py
│   └── transaction_service.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── ml/
│   ├── models/
│   │   ├── RF_100.joblib
│   │   ├── RF_300.joblib
│   │   ├── RF_DEEPER.joblib
│   │   ├── baseline_logistic_regression.joblib
│   │   └── sentinel_random_forest.joblib
│   │
│   └── src/
│       ├── compare_rf_models.py
│       ├── eda.py
│       ├── evaluate_deeper_thresholds.py
│       ├── evaluate_rf_thresholds.py
│       ├── evaluate_thresholds.py
│       ├── feature_importance.py
│       ├── final_evaluation.py
│       ├── prepare_data.py
│       ├── train_baseline.py
│       └── train_random_forest.py
│
├── data/
│   └── processed/
│
├── package.json
├── package-lock.json
├── README.md
└── .gitignore