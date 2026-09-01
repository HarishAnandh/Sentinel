
# 🛡️ Sentinel — AI Risk Manager

### AI-Powered Fraud Detection & Transaction Risk Intelligence

Sentinel is an AI-powered transaction risk management platform designed to help merchants detect potentially fraudulent transactions before they result in financial loss through fraud, chargebacks, and transaction abuse.

The platform combines a calibrated Machine Learning model with a real-time risk engine, transaction simulation, risk queue, analytics dashboard, and batch CSV analysis.

---

## 🚀 Live Demo

### Frontend
https://sentinel-tawny-psi.vercel.app

### Backend API
https://sentinel1-wqdp.onrender.com

### API Documentation
https://sentinel1-wqdp.onrender.com/docs

---

# 🎯 Project Objective

Sentinel aims to provide merchants with an intelligent and explainable fraud-risk assessment system.

### Key objectives

- Detect potentially fraudulent transactions using Machine Learning.
- Convert model predictions into an interpretable risk score from 0–100.
- Classify transactions into LOW, MEDIUM, and HIGH risk.
- Automatically recommend actions such as `APPROVE` or `HOLD_AND_VERIFY`.
- Reduce unnecessary false-positive alerts.
- Provide explainable risk signals using feature importance.
- Support real-time transaction assessment through REST APIs.
- Support batch fraud analysis through CSV uploads.
- Provide a visual risk queue for high-risk transactions.
- Allow users to simulate transaction scenarios and observe risk changes.
- Provide measurable model performance using a held-out test set.

---

# 💡 Why Sentinel?

Traditional rule-based fraud systems often struggle with:

- Increasing transaction volume
- Complex fraud patterns
- False-positive alerts
- Manual investigation overhead
- Lack of explainability
- Difficulty adapting to changing transaction behavior

Sentinel addresses these challenges by combining Machine Learning with a transparent risk-management layer.

Instead of simply returning:

> Fraud / Not Fraud

Sentinel provides:

> **Risk Score → Probability → Risk Level → Decision → Risk Signals**

This makes the system more useful for an actual merchant risk-management workflow.

---

# 🧠 Machine Learning Model

Sentinel uses a **Random Forest-based fraud detection model** trained on transaction-level fraud data.

The final production model uses probability calibration to produce more meaningful fraud-risk probabilities.

### Production model

```text
RF_DEEPER_CALIBRATED
````

### Model pipeline

```text
Transaction
     ↓
Feature Extraction
     ↓
Random Forest Model
     ↓
Probability Calibration
     ↓
Fraud Probability
     ↓
Risk Score (0–100)
     ↓
Risk Classification
     ↓
Recommended Action
```

---

# 📊 Model Performance

Sentinel evaluates its model using a **held-out test dataset**, rather than reporting training performance.

### Final evaluation

| Metric             |        Result |
| ------------------ | ------------: |
| Precision          |    **94.94%** |
| Recall             |    **76.53%** |
| F1 Score           |    **84.75%** |
| ROC-AUC            |    **97.02%** |
| PR-AUC             |    **86.43%** |
| Test Transactions  |    **56,962** |
| Actual Fraud Cases |        **98** |
| Fraud Detected     |   **75 / 98** |
| False Positives    |         **4** |
| False Alert Rate   | **0.007034%** |
| Decision Threshold |      **0.60** |

The model prioritizes **high precision** to reduce unnecessary fraud alerts while maintaining useful fraud detection coverage.

---

# 📈 Precision Optimization History

During development, Sentinel's model performance and decision threshold were iteratively evaluated.

The initial dashboard reported:

```text
Precision: 85.42%
```

After model calibration, threshold evaluation, and refinement of the final production configuration, the reported precision improved to:

```text
Precision: 94.94%
```

This improvement was achieved by evaluating different Random Forest configurations, calibration strategies, and fraud-decision thresholds on held-out validation/test data.

The goal was not simply to maximize one metric, but to find a practical balance between:

* Precision
* Recall
* F1 Score
* False-positive rate
* Fraud detection coverage

This resulted in the final production decision threshold of:

```text
0.60
```

---

# ⚙️ Risk Engine

Sentinel converts the model's fraud probability into an actionable risk score.

```text
Risk Score = Fraud Probability × 100
```

### Risk classification

```text
0–29.99    → LOW
30–69.99   → MEDIUM
70–100     → HIGH
```

### Decision logic

```text
Probability < 0.60
        ↓
     APPROVE

Probability ≥ 0.60
        ↓
 HOLD_AND_VERIFY
```

This separates the ML prediction from the business decision layer.

---

# 🔎 Explainable Risk Signals

Sentinel does not only provide a fraud probability.

The Risk Engine also identifies important transaction features contributing to the model's decision.

Example:

```text
Top Risk Signals

V14  → 18.33%
V10  → 11.46%
V4   → 11.42%
V12  → 9.87%
V17  → 8.94%
```

Each signal is displayed with:

* Feature name
* Feature value
* Model importance
* Impact percentage
* Signal severity

This provides a basic explainability layer for fraud analysts.

---

# 📊 CSV Transaction Analyzer

Sentinel supports **batch transaction analysis through CSV uploads**.

Users can navigate to the **CSV Analyzer** page and upload a compatible transaction dataset.

### Required columns

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

The uploaded CSV is processed by the production fraud-risk model.

### CSV Analyzer provides

* Total transactions analyzed
* High-risk transactions
* Medium-risk transactions
* Low-risk transactions
* Fraud alerts
* Average risk score
* Fraud probability for each transaction
* Risk classification
* Recommended decision

### Example workflow

```text
Upload CSV
     ↓
Validate Required Columns
     ↓
Load Transaction Data
     ↓
Run ML Predictions
     ↓
Calculate Risk Scores
     ↓
Classify Risk
     ↓
Generate Fraud Alerts
     ↓
Display Results
```

A sample CSV is included in the repository:

```text
data/sample/sample_transactions.csv
```

The raw source dataset is intentionally not committed to the repository to keep the project lightweight.

---

# 🧪 Transaction Simulation

Sentinel includes an interactive transaction simulator.

Users can modify transaction characteristics such as:

* Transaction amount
* Transaction time
* Device status
* Transaction frequency
* Unusual transaction timing

These inputs are transformed into the model's feature space and passed through the same risk engine.

This allows users to observe how changes in transaction behavior can affect the resulting risk assessment.

---

# 🚨 Risk Queue

The Risk Queue provides a centralized view of potentially dangerous transactions.

Transactions can be reviewed based on:

* Risk score
* Risk probability
* Risk level
* Recommended action
* Important risk signals

This provides a workflow closer to how a merchant fraud analyst would investigate suspicious transactions.

---

# 📊 Analytics Dashboard

The Analytics page provides an overview of model performance and risk intelligence.

It includes:

* Precision
* Recall
* F1 Score
* ROC-AUC
* Test transaction count
* Fraud cases
* Fraud detection coverage
* False alerts
* False alert rate
* Active model
* Top risk signals

This allows the user to understand both the **ML performance** and the **operational impact** of the model.

---

# 🏗️ System Architecture

```text
                     SENTINEL
                         │
                         ▼
              ┌────────────────────┐
              │    React Frontend  │
              │      + Vite        │
              └─────────┬──────────┘
                        │
                        │ REST API
                        ▼
              ┌────────────────────┐
              │   FastAPI Backend  │
              └─────────┬──────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   Risk Engine     CSV Analyzer   Simulation
          │             │
          └──────┬──────┘
                 ▼
        ┌───────────────────┐
        │ Calibrated Random │
        │   Forest Model    │
        └─────────┬─────────┘
                  │
                  ▼
          Fraud Probability
                  │
                  ▼
            Risk Score
                  │
                  ▼
          Risk Classification
                  │
                  ▼
        Recommended Decision
```

---

# 🛠️ Technology Stack

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
* Python Multipart

## Machine Learning

* Scikit-learn
* Random Forest
* Probability Calibration
* Pandas
* NumPy
* Joblib

## Deployment

* Vercel — Frontend
* Render — Backend API
* GitHub — Source Code & Version Control

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
├── data/
│   ├── processed/
│   └── sample/
│       └── sample_transactions.csv
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   ├── Simulation.jsx
│   │   ├── Simulation.css
│   │   ├── CSVAnalyzer.jsx
│   │   └── CSVAnalyzer.css
│   └── package.json
│
├── ml/
│   ├── models/
│   │   └── RF_DEEPER_CALIBRATED.joblib
│   │
│   └── src/
│       ├── calibrate_model.py
│       ├── evaluate_calibrated_test.py
│       ├── train_random_forest.py
│       ├── evaluate_thresholds.py
│       └── final_evaluation.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /health
```

Returns the backend and model status.

---

## Normal Transaction Demo

```http
GET /api/v1/demo/normal
```

Returns a sample low-risk transaction.

---

## Fraud Transaction Demo

```http
GET /api/v1/demo/fraud
```

Returns a sample high-risk transaction.

---

## Risk Assessment

```http
POST /api/v1/risk/assess
```

Accepts a transaction and returns its risk assessment.

---

## Transaction Simulation

```http
POST /api/v1/simulation
```

Runs a simulated transaction through the risk engine.

---

## CSV Analysis

```http
POST /api/v1/analyze/csv
```

Accepts a CSV file and performs batch fraud-risk analysis.

---

# 💻 Local Development

## 1. Clone the repository

```bash
git clone https://github.com/HarishAnandh/Sentinel.git
cd Sentinel
```

---

## 2. Create virtual environment

```bash
python -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

---

## 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

Make sure multipart support is installed:

```bash
pip install python-multipart
```

---

## 4. Start FastAPI

From the project root:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Frontend Development

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

The Vite development server will provide the local frontend URL.

---

# 🧪 Testing the CSV Analyzer

Example:

```bash
curl -X POST \
  -F "file=@data/sample/sample_transactions.csv" \
  http://127.0.0.1:8000/api/v1/analyze/csv
```

Production API:

```bash
curl -X POST \
  -F "file=@data/sample/sample_transactions.csv" \
  https://sentinel1-wqdp.onrender.com/api/v1/analyze/csv
```

---

# 🌐 Production Deployment

### Frontend

Deployed using:

```text
Vercel
```

Live application:

[https://sentinel-tawny-psi.vercel.app](https://sentinel-tawny-psi.vercel.app)

### Backend

Deployed using:

```text
Render
```

Production API:

[https://sentinel1-wqdp.onrender.com](https://sentinel1-wqdp.onrender.com)

The frontend communicates with the deployed FastAPI backend through REST APIs.

---

# ⚠️ Browser Troubleshooting

Sentinel does **not** require Incognito/Private browsing.

During development and production testing, a browser-side issue was observed where the CSV Analyzer could occasionally display:

```text
ERR_NETWORK_CHANGED
```

along with an asynchronous browser listener message.

The application worked correctly in an Incognito/Private window, indicating that the issue was browser-session or extension related rather than a Sentinel backend/model failure.

If the CSV Analyzer does not work in a normal browser session:

1. Try a hard refresh.
2. Temporarily disable browser extensions.
3. Clear the site's cached data.
4. Try an Incognito/Private window.

> **Incognito mode is only a troubleshooting workaround and is not required for Sentinel.**

---

# 🔐 Data & Repository Notes

The repository intentionally excludes:

* Raw datasets
* Python virtual environments
* Node modules
* Build output
* Python cache files
* Other unnecessary generated files

The project includes the processed evaluation artifacts and production ML model required to demonstrate the fraud-risk system.

---

# 🎯 Key Highlights

### 🤖 Machine Learning

Calibrated Random Forest fraud detection model.

### 📈 High Precision

Final evaluated precision of **94.94%**.

### 🎯 Risk Scoring

Converts fraud probabilities into an intuitive 0–100 risk score.

### 🚨 Actionable Decisions

Automatically recommends:

```text
APPROVE
HOLD_AND_VERIFY
```

### 🔎 Explainability

Provides important feature-level risk signals.

### 📂 Batch Analysis

Users can upload compatible CSV datasets and analyze multiple transactions at once.

### 🧪 Simulation

Interactive transaction-risk simulation.

### 📊 Analytics

Dedicated model-performance and risk-intelligence dashboard.

### 🌐 Production Ready

React frontend deployed on Vercel with FastAPI backend deployed on Render.

---

# 🏆 Project Vision

Sentinel is designed around a simple principle:

> **Don't just detect fraud — help merchants make better risk decisions.**

The system combines machine learning, probability calibration, explainability, batch analysis, simulation, and actionable decision logic into a single merchant-focused risk management platform.

---

# 👨‍💻 Team / Project

**Sentinel — AI Risk Manager**

Built as an AI/ML-focused fraud risk management solution for merchant transaction protection.

---

## ⭐ Repository

[https://github.com/HarishAnandh/Sentinel](https://github.com/HarishAnandh/Sentinel)

If you find the project interesting, consider giving the repository a ⭐.


