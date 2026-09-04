
# 🛡️ Sentinel — AI Risk Manager

### AI-Powered Merchant Fraud Detection, Risk Assessment & Transaction Intelligence

Sentinel is an AI-powered risk management platform designed to help merchants identify potentially fraudulent transactions before they result in financial losses.

The system combines a **calibrated Random Forest fraud detection model**, real-time transaction assessment, batch CSV analysis, risk scoring, transaction simulation, and an interactive risk dashboard.

Instead of simply returning a binary `fraud / not fraud` prediction, Sentinel converts model output into an actionable risk decision:

> **APPROVE → REVIEW → HOLD & VERIFY**

---

## 🚀 Live Demo

### Frontend

🔗 https://sentinel-tawny-psi.vercel.app

### Backend API

🔗 https://sentinel1-wqdp.onrender.com

The frontend is deployed on **Vercel**, while the FastAPI backend and machine-learning inference engine are deployed on **Render**.

---

# 🎯 Problem Statement

Fraud, chargebacks, transaction abuse, and suspicious payment activity can silently reduce merchant margins.

Traditional fraud detection systems often provide only a binary prediction, making it difficult for merchants to understand:

- How risky a transaction actually is
- Why a transaction was flagged
- Which signals contributed to the risk
- Whether the transaction should be approved or manually verified
- How an entire batch of transactions is performing

Sentinel addresses this by providing an **interpretable transaction-risk workflow** rather than just a raw ML prediction.

---

# 💡 Solution

Sentinel evaluates transaction data using a trained and calibrated Random Forest model.

The model generates a fraud probability, which is converted into:

- Risk Score
- Risk Level
- Decision
- Risk Signals
- Feature Importance

The platform also supports **batch CSV analysis**, allowing merchants to upload multiple transactions and receive a complete risk analysis.

---

# ✨ Key Features

## 🔍 1. Real-Time Transaction Risk Assessment

Analyze individual transactions through the risk engine.

Each transaction receives:

- Fraud probability
- Risk score
- Risk level
- Recommended action
- Important risk signals

Example:

```text
Risk Score       : 98.28 / 100
Risk Probability : 0.9828
Risk Level       : HIGH
Decision         : HOLD_AND_VERIFY
````

---

## 📊 2. Risk Classification

Sentinel converts fraud probability into three risk categories:

| Risk Score | Risk Level |
| ---------- | ---------- |
| 0–29.99    | LOW        |
| 30–69.99   | MEDIUM     |
| 70–100     | HIGH       |

This gives merchants a simple way to prioritize suspicious transactions.

---

# 🚦 3. Decision Engine

Sentinel translates the model probability into an operational decision.

```text
Low probability
       ↓
   APPROVE

Higher probability
       ↓
 HOLD_AND_VERIFY
```

The current fraud decision threshold is:

```text
0.60
```

Transactions with fraud probability ≥ `0.60` are flagged for verification.

---

# 🧠 4. Calibrated Machine Learning Model

Sentinel uses a **Random Forest classifier with probability calibration**.

The model development process included:

1. Baseline Logistic Regression
2. Random Forest experimentation
3. Multiple Random Forest configurations
4. Threshold evaluation
5. Deeper Random Forest evaluation
6. Probability calibration
7. Hold-out test evaluation
8. Integration into the production risk engine

The production model is:

```text
RF_DEEPER_CALIBRATED
```

Model artifact:

```text
ml/models/RF_DEEPER_CALIBRATED.joblib
```

---

# 📈 5. Model Performance

The model was evaluated using a held-out test dataset.

Current dashboard metrics:

| Metric             | Performance |
| ------------------ | ----------- |
| Precision          | 94%+        |
| Recall             | ~84%        |
| F1 Score           | ~89%        |
| ROC-AUC            | ~97%        |
| Test Transactions  | 56,962      |
| Actual Fraud Cases | 98          |

> The exact values displayed in the dashboard represent the final evaluation configuration used by Sentinel.

---

# 🔄 Precision Improvement

An important part of Sentinel's development was improving the quality of fraud alerts.

The initial dashboard configuration reported approximately:

```text
Precision: 85.42%
```

After further model evaluation, calibration, and threshold analysis, the system was improved to achieve approximately:

```text
Precision: 94%+
```

This improvement was important because fraud detection is not only about detecting fraud cases.

It is also about reducing unnecessary alerts.

### Why Precision Matters

Low precision means the system can generate many false alerts.

For a merchant, excessive false positives can result in:

* Legitimate transactions being blocked
* Customer frustration
* Increased manual review
* Operational overhead

Improving precision makes Sentinel more practical as a merchant-facing risk management system.

---

# 📊 6. CSV Transaction Analyzer

Sentinel supports **batch transaction analysis through CSV upload**.

Users can upload a CSV containing transaction records, and Sentinel processes the entire dataset through the production risk engine.

### Required Columns

The CSV should contain:

```text
Time
V1
V2
V3
V4
V5
V6
V7
V8
V9
V10
V11
V12
V13
V14
V15
V16
V17
V18
V19
V20
V21
V22
V23
V24
V25
V26
V27
V28
Amount
```

A ready-to-use sample dataset is included in:

```text
data/sample/sample_transactions.csv
```

### CSV Analysis Output

For every transaction, Sentinel generates:

* Fraud probability
* Risk score
* Risk level
* Decision

The batch analysis also provides:

* Total transactions
* High-risk transactions
* Medium-risk transactions
* Low-risk transactions
* Fraud alerts
* Average risk score

This allows merchants to analyze an entire transaction file instead of processing transactions individually.

---

# 🧪 7. Transaction Simulation

Sentinel includes an interactive transaction simulator.

Users can modify factors such as:

* Transaction amount
* Device status
* Transaction frequency
* Unusual transaction time

The simulator converts these inputs into a transaction feature vector and sends it to the risk engine.

This demonstrates how changing transaction characteristics can affect the resulting risk assessment.

---

# 🚨 8. Risk Queue

The Risk Queue provides a centralized view of suspicious transactions.

It helps prioritize transactions that require manual verification.

High-risk transactions can be reviewed based on:

* Risk score
* Risk level
* Fraud probability
* Decision
* Transaction details

---

# 📉 9. Analytics Dashboard

The Analytics section provides model and risk intelligence.

It includes:

* Precision
* Recall
* F1 Score
* ROC-AUC
* Test transaction count
* Actual fraud cases
* Fraud detected
* False alerts
* False alert rate
* Active model

The dashboard also displays the most important Random Forest features.

### Top Risk Signals

The current model identifies signals such as:

```text
V14
V10
V4
V12
V17
```

These are presented using feature-importance visualizations.

---

# 🔎 10. Explainable Risk Signals

Sentinel does not stop at:

```text
"This transaction is fraudulent."
```

Instead, the risk engine provides important model signals.

Example:

```json
{
  "feature": "V14",
  "value": -7.2455,
  "importance": 0.1833,
  "impact": 18.3,
  "severity": "Strong signal"
}
```

This provides additional context for why a transaction received a particular risk assessment.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      Merchant        │
                    │       / User         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    React Frontend    │
                    │       Vite           │
                    │      Vercel          │
                    └──────────┬───────────┘
                               │
                     REST API Requests
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │       Render         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Sentinel Risk      │
                    │       Engine         │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │ RF_DEEPER_CALIBRATED Model     │
              │                                │
              │ Random Forest + Calibration    │
              └───────────────┬────────────────┘
                              │
                              ▼
                  ┌─────────────────────┐
                  │ Fraud Probability   │
                  │ Risk Score          │
                  │ Risk Level          │
                  │ Decision            │
                  │ Risk Signals        │
                  └─────────────────────┘
```

---

# 🧰 Technology Stack

## Frontend

* React.js
* Vite
* JavaScript
* CSS
* Lucide React

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* Pandas
* python-multipart

## Machine Learning

* Scikit-learn
* Random Forest
* CalibratedClassifierCV
* NumPy
* Pandas
* Joblib

## Deployment

* Vercel — Frontend
* Render — Backend API
* GitHub — Source Control

---

# 📁 Project Structure

```text
Sentinel/
│
├── app/
│   ├── main.py
│   ├── risk_engine.py
│   ├── transaction_service.py
│   └── csv_analyzer.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── CSVAnalyzer.jsx
│   │   ├── CSVAnalyzer.css
│   │   ├── Simulation.jsx
│   │   ├── Simulation.css
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
│   │   ├── RF_DEEPER_CALIBRATED.joblib
│   │   ├── baseline_logistic_regression.joblib
│   │   └── sentinel_random_forest.joblib
│   │
│   └── src/
│       ├── calibrate_model.py
│       ├── compare_rf_models.py
│       ├── eda.py
│       ├── evaluate_calibrated_test.py
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
│   ├── sample/
│   │   └── sample_transactions.csv
│   │
│   └── processed/
│       ├── calibrated_test_results.csv
│       ├── deeper_threshold_results.csv
│       ├── feature_importance.csv
│       ├── final_test_results.csv
│       ├── rf_threshold_results.csv
│       ├── test.csv
│       ├── threshold_results.csv
│       └── validation.csv
│
├── package.json
├── package-lock.json
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔌 API Endpoints

## Root

```http
GET /
```

Returns service status.

---

## Health Check

```http
GET /health
```

Example:

```json
{
  "status": "healthy",
  "model": "RF_DEEPER",
  "model_loaded": true
}
```

---

## Assess Transaction

```http
POST /api/v1/risk/assess
```

Accepts a transaction containing:

```text
Time
V1-V28
Amount
```

Returns the risk assessment.

---

## Demo Normal Transaction

```http
GET /api/v1/demo/normal
```

Returns a sample low-risk transaction.

---

## Demo Fraud Transaction

```http
GET /api/v1/demo/fraud
```

Returns a sample high-risk transaction.

---

## Transaction Simulation

```http
POST /api/v1/simulation
```

Accepts simulation parameters and returns the resulting risk assessment.

---

## CSV Analysis

```http
POST /api/v1/analyze/csv
```

Accepts a CSV file through multipart form upload.

Example:

```bash
curl -X POST \
  -F "file=@data/sample/sample_transactions.csv" \
  https://sentinel1-wqdp.onrender.com/api/v1/analyze/csv
```

---

# 💻 Running Sentinel Locally

## 1. Clone the Repository

```bash
git clone https://github.com/HarishAnandh/Sentinel.git
cd Sentinel
```

---

# 🐍 Backend Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# ⚛️ Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will provide a local URL, typically:

```text
http://localhost:5173
```

---

# 📊 Testing the CSV Analyzer Locally

After starting the backend, use the included sample file:

```text
data/sample/sample_transactions.csv
```

You can test the API using:

```bash
curl -X POST \
  -F "file=@data/sample/sample_transactions.csv" \
  http://127.0.0.1:8000/api/v1/analyze/csv
```

The response contains both batch-level statistics and transaction-level risk results.

---

# 🧪 Machine Learning Pipeline

The ML development process follows a structured workflow:

```text
Raw Credit Card Dataset
          │
          ▼
     Data Preparation
          │
          ▼
   Exploratory Analysis
          │
          ▼
 Baseline Model Training
          │
          ▼
 Random Forest Training
          │
          ▼
 Model Comparison
          │
          ▼
 Threshold Evaluation
          │
          ▼
 Deeper RF Evaluation
          │
          ▼
 Probability Calibration
          │
          ▼
 Hold-Out Test Evaluation
          │
          ▼
 Production Risk Engine
```

---

# 📚 ML Development Files

### Data Preparation

```text
ml/src/prepare_data.py
```

Prepares the dataset for training and evaluation.

### Baseline Model

```text
ml/src/train_baseline.py
```

Creates the baseline Logistic Regression model.

### Random Forest

```text
ml/src/train_random_forest.py
```

Trains Random Forest models.

### Model Comparison

```text
ml/src/compare_rf_models.py
```

Compares different Random Forest configurations.

### Threshold Evaluation

```text
ml/src/evaluate_thresholds.py
ml/src/evaluate_rf_thresholds.py
ml/src/evaluate_deeper_thresholds.py
```

Evaluates different probability thresholds and their effect on model performance.

### Calibration

```text
ml/src/calibrate_model.py
```

Calibrates the Random Forest probability estimates.

### Calibrated Evaluation

```text
ml/src/evaluate_calibrated_test.py
```

Evaluates the calibrated model on the test dataset.

### Feature Importance

```text
ml/src/feature_importance.py
```

Extracts the most influential model features.

---

# 🧱 Build Challenges & Technical Obstacles

Building Sentinel involved several practical engineering challenges.

## 1. Probability Calibration

The Random Forest model's raw probabilities were not initially sufficient for a production-style risk scoring system.

A calibration stage was introduced to make probability estimates more useful for downstream decision-making.

---

## 2. Precision vs Recall Trade-off

Fraud detection requires balancing:

```text
Detecting more fraud
        ↕
Avoiding unnecessary alerts
```

Different thresholds were evaluated to find a more practical operating point.

This eventually contributed to improving precision from approximately **85% to 94%+**.

---

## 3. CalibratedClassifierCV Feature Importance

One technical issue occurred when the production model was changed from a normal Random Forest to:

```text
CalibratedClassifierCV
```

Unlike Random Forest, `CalibratedClassifierCV` does not directly expose:

```python
feature_importances_
```

The risk engine initially failed with:

```text
AttributeError:
'CalibratedClassifierCV' object has no attribute 'feature_importances_'
```

The feature-importance logic was therefore adapted to work with the underlying calibrated estimator.

---

## 4. FastAPI Application Structure

The project initially experienced an import issue when running:

```bash
uvicorn app.main:app --reload
```

The backend structure was reorganized so that the application could correctly load:

```text
app.main:app
```

---

## 5. CSV Upload Support

Adding CSV upload introduced a multipart form-data dependency.

FastAPI requires:

```text
python-multipart
```

for file uploads.

The dependency was added to the project requirements and the CSV Analyzer was integrated into the API.

---

## 6. Production API Connectivity

The frontend initially used:

```text
http://127.0.0.1:8000
```

which works only on the local machine.

For production deployment, the frontend was updated to communicate with the Render backend:

```text
https://sentinel1-wqdp.onrender.com
```

This allowed the Vercel deployment to communicate with the production FastAPI server.

---

# 🌐 Deployment Architecture

```text
GitHub
   │
   ├───────────────┐
   │               │
   ▼               ▼
Vercel           Render
   │               │
React App      FastAPI API
   │               │
   └───────┬───────┘
           │
           ▼
   Sentinel Risk Engine
           │
           ▼
RF_DEEPER_CALIBRATED
```

---

# 🌍 Deployment Notes

### Frontend

Hosted on:

```text
Vercel
```

Live URL:

```text
https://sentinel-tawny-psi.vercel.app
```

### Backend

Hosted on:

```text
Render
```

API URL:

```text
https://sentinel1-wqdp.onrender.com
```

The frontend communicates with the production backend using REST APIs.

---

# 🕵️ CSV Analyzer Browser Note

The CSV Analyzer works in the deployed application.

If the browser occasionally shows errors such as:

```text
ERR_NETWORK_CHANGED
```

or the CSV request fails unexpectedly, try opening Sentinel in an **Incognito / Private browser window**.

Browser extensions, cached connections, or an existing browser session can sometimes interfere with the request.

The Incognito window provides a clean browser session for testing the deployed CSV upload functionality.

---

# 🔐 Security Considerations

Sentinel is designed as a prototype risk-management system.

For a production financial deployment, additional security layers would be required, including:

* Authentication
* Authorization
* Rate limiting
* API key management
* Secure file validation
* File-size limits
* Input sanitization
* Audit logging
* Encryption
* PII protection
* Model monitoring
* Data drift detection

---

# 📌 Current Scope

Sentinel currently focuses on transaction-level fraud risk assessment using the credit-card transaction feature representation:

```text
Time
V1-V28
Amount
```

The system demonstrates the complete workflow:

```text
Transaction
     ↓
ML Prediction
     ↓
Fraud Probability
     ↓
Risk Score
     ↓
Risk Classification
     ↓
Decision
     ↓
Merchant Action
```

---

# 🔮 Future Improvements

Potential future enhancements include:

* Explainable AI using SHAP
* Real merchant transaction integrations
* Streaming fraud detection
* Real-time fraud spike detection
* Device fingerprinting
* User behavioral profiling
* Account takeover detection
* Chargeback prediction
* Return-abuse detection
* Fraud ring detection
* Model drift monitoring
* Automated retraining
* Feedback-driven model improvement
* Database-backed transaction history
* Role-based merchant access
* Advanced alert management

---

# 🎯 Why Sentinel?

Sentinel is designed around a simple principle:

> **Don't just detect fraud. Help merchants decide what to do about risk.**

Instead of producing only a prediction, Sentinel converts machine-learning output into an operational risk workflow.

```text
                    SENTINEL
                       │
            ┌──────────┴──────────┐
            │                     │
       Detection             Intelligence
            │                     │
            ▼                     ▼
     Fraud Probability      Risk Signals
            │                     │
            └──────────┬──────────┘
                       │
                       ▼
                  Risk Score
                       │
                       ▼
                Risk Classification
                       │
                       ▼
                 Decision Engine
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          APPROVE          HOLD & VERIFY
```

---

# 👨‍💻 Project

**Sentinel — AI Risk Manager**

Built as an AI/ML risk-management platform focused on practical merchant fraud detection and decision support.

### Repository

[https://github.com/HarishAnandh/Sentinel](https://github.com/HarishAnandh/Sentinel)

### Live Application

[https://sentinel-tawny-psi.vercel.app](https://sentinel-tawny-psi.vercel.app)

### Backend API

[https://sentinel1-wqdp.onrender.com](https://sentinel1-wqdp.onrender.com)

---

# ⭐ Acknowledgement

Built with:

* Python
* FastAPI
* Scikit-learn
* Random Forest
* React
* Vite
* Vercel
* Render
* GitHub

---

## 🛡️ Sentinel

### Detect risk. Understand signals. Protect transactions.


