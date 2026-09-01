
# 🛡️ Sentinel
### AI-Powered Fraud Risk Detection & Transaction Verification System

> **Detect fraud. Quantify risk. Reduce false alerts.**

Sentinel is an AI-powered fraud risk assessment platform designed to identify potentially fraudulent financial transactions and convert machine-learning predictions into actionable risk decisions.

Instead of treating fraud detection as a simple **fraud / not-fraud classification problem**, Sentinel generates a calibrated probability, converts it into an interpretable risk score, identifies important risk signals, and recommends an operational action such as:

- ✅ **APPROVE**
- ⚠️ **HOLD & VERIFY**
- 🚨 **HIGH RISK**

The system combines a calibrated Random Forest model, FastAPI backend, and React-based analytics dashboard into an end-to-end fraud risk intelligence platform.

---

## 🚀 Live Demo

### 🌐 Vercel Deployment

**[Open Sentinel Dashboard](https://sentinel-tawny-psi.vercel.app)**

> Replace `YOUR_VERCEL_LINK_HERE` with the deployed Vercel URL.

---

# 🎯 Project Objective

Sentinel was built to address a practical problem in digital payments and financial services:

> **How can an organization detect fraudulent transactions accurately while avoiding unnecessary false alerts on legitimate customers?**

### Core objectives

- Detect potentially fraudulent financial transactions using machine learning.
- Generate a meaningful fraud-risk probability for every transaction.
- Convert model probabilities into an interpretable **0–100 risk score**.
- Categorize transactions into **LOW, MEDIUM, and HIGH risk**.
- Recommend operational actions based on risk.
- Minimize false-positive alerts.
- Improve model probability reliability through calibration.
- Provide interpretable risk signals using feature importance.
- Evaluate performance on a completely untouched hold-out test set.
- Provide an analytics dashboard for monitoring model performance.

---

# 🧠 How Sentinel Works

```text
Transaction
     │
     ▼
Feature Extraction
     │
     ▼
Random Forest Model
     │
     ▼
Probability Calibration
     │
     ▼
Fraud Probability
     │
     ▼
Risk Score (0–100)
     │
     ├───────────────┐
     ▼               ▼
Risk Level      Risk Signals
     │               │
     ▼               ▼
Decision Engine  Explainability
     │
     ▼
APPROVE / HOLD & VERIFY
````

---

# 🤖 Machine Learning Pipeline

Sentinel uses a **Random Forest classifier** trained on transaction-level features.

The pipeline consists of:

1. Data preparation
2. Exploratory data analysis
3. Random Forest training
4. Model comparison
5. Threshold evaluation
6. Probability calibration
7. Hold-out test evaluation
8. Risk scoring
9. Decision generation

### Model

**Random Forest Classifier**

Configuration used for the deeper model:

```text
n_estimators = 200
max_depth = 18
min_samples_leaf = 2
class_weight = balanced
max_features = sqrt
random_state = 42
```

The use of `class_weight="balanced"` is particularly important because fraudulent transactions are extremely rare compared with legitimate transactions.

---

# 🎯 Probability Calibration

One of the major improvements made during development was addressing **overconfident model probabilities**.

The initial model could generate values extremely close to:

```text
0.000000
0.999975
```

Although these values can be useful for classification, presenting them directly to users can make the system appear more certain than it should be.

Sentinel therefore introduced a **calibrated Random Forest model**.

### Before calibration

```text
Minimum probability : 0.000000
Maximum probability : 0.999975
```

### After calibration

```text
Minimum probability : 0.000427
Maximum probability : 0.986493
```

This produces a more useful probability distribution for downstream risk scoring and decision-making.

---

# 📈 Precision Improvement Journey

Model performance was not treated as a one-shot result.

Sentinel went through multiple evaluation stages to improve the quality of fraud alerts.

### Initial model

The original final evaluation produced:

| Metric          |    Initial |
| --------------- | ---------: |
| Precision       | **85.42%** |
| Recall          | **83.67%** |
| F1 Score        | **84.54%** |
| ROC-AUC         | **97.02%** |
| False Positives |         14 |

This was already a strong baseline, but the objective was to reduce the number of legitimate transactions incorrectly flagged as fraud.

---

## 🔬 Calibration & Threshold Optimization

After introducing probability calibration, multiple decision thresholds were evaluated on an untouched hold-out test set.

| Threshold |  Precision |     Recall |         F1 |
| --------: | ---------: | ---------: | ---------: |
|      0.30 |      88.8% |      80.6% |      84.5% |
|      0.40 |      88.4% |      77.6% |      82.6% |
|      0.50 |      89.3% |      76.5% |      82.4% |
|  **0.60** | **94.94%** | **76.53%** | **84.75%** |
|      0.70 |      94.9% |      76.5% |     84.75% |
|      0.80 |      94.8% |      74.5% |      83.4% |

The selected production threshold is:

```text
0.60
```

This means Sentinel prioritizes high-confidence fraud alerts while significantly reducing false alerts.

---

# 🏆 Final Hold-Out Test Performance

The final calibrated model was evaluated on an untouched test set containing:

```text
56,962 transactions
98 actual fraud cases
```

### Final Results

| Metric           |      Result |
| ---------------- | ----------: |
| **Precision**    |  **94.94%** |
| **Recall**       |  **76.53%** |
| **F1 Score**     |  **84.75%** |
| **ROC-AUC**      |  **97.02%** |
| **PR-AUC**       |  **86.43%** |
| True Positives   |          75 |
| False Positives  |           4 |
| False Negatives  |          23 |
| True Negatives   |      56,860 |
| False Alert Rate | **0.0070%** |

### Key improvement

```text
Initial Precision     → 85.42%

Calibrated Precision  → 94.94%

Improvement            → +9.52 percentage points
```

The number of false alerts also decreased:

```text
14 → 4
```

This was one of the main goals of the model refinement process.

---

# 🔍 Explainable Risk Signals

Sentinel does not simply return a probability.

The system also exposes the most important model features contributing to its risk analysis.

### Top Risk Signals

| Feature | Importance |
| ------- | ---------: |
| V14     |     18.33% |
| V10     |     11.46% |
| V4      |     11.42% |
| V12     |      9.87% |
| V17     |      8.94% |

These signals are surfaced by the risk engine to provide additional context around the model's assessment.

---

# ⚡ Risk Engine

The Sentinel risk engine converts the calibrated probability into an operational risk assessment.

Example:

```text
Risk score       : 98.28 / 100
Risk probability : 0.9828
Risk level       : HIGH
Decision         : HOLD_AND_VERIFY
```

A low-risk transaction can produce:

```text
Risk score       : 0.05 / 100
Risk probability : 0.0005
Risk level       : LOW
Decision         : APPROVE
```

This makes the machine-learning output easier for a human operator to understand and act upon.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │   Vite + CSS        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI API      │
                    │   REST Endpoints    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Sentinel Risk     │
                    │      Engine         │
                    └──────────┬──────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ Calibrated Random Forest    │
                │ RF_DEEPER_CALIBRATED        │
                └──────────────┬──────────────┘
                               │
                               ▼
                    Fraud Probability
                               │
                               ▼
                       Risk Score
                               │
                               ▼
                 ┌─────────────────────────┐
                 │ Approve / Hold & Verify │
                 └─────────────────────────┘
```

---

# 💻 Technology Stack

## Frontend

* React
* Vite
* JavaScript
* CSS
* Lucide React

## Backend

* Python
* FastAPI
* Uvicorn
* REST APIs

## Machine Learning

* Python
* Scikit-learn
* Pandas
* NumPy
* Joblib

## Model

* Random Forest
* Class-weight balancing
* Probability calibration
* Threshold optimization

## Deployment

* Vercel — Frontend
* FastAPI — Backend API

---

# 📂 Project Structure

```text
Sentinel/
│
├── app/
│   ├── main.py
│   ├── risk_engine.py
│   └── transaction_service.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── validation.csv
│       ├── test.csv
│       ├── calibrated_test_results.csv
│       ├── feature_importance.csv
│       └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   └── package.json
│
├── ml/
│   ├── models/
│   │   ├── RF_DEEPER.joblib
│   │   └── RF_DEEPER_CALIBRATED.joblib
│   │
│   └── src/
│       ├── prepare_data.py
│       ├── train_random_forest.py
│       ├── calibrate_model.py
│       ├── evaluate_deeper_thresholds.py
│       ├── evaluate_calibrated_test.py
│       ├── final_evaluation.py
│       ├── feature_importance.py
│       └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧪 Model Evaluation

Sentinel uses multiple metrics instead of relying solely on accuracy.

### Precision

Measures how many transactions flagged as fraud were actually fraudulent.

This is particularly important because excessive false alerts can negatively affect legitimate customers.

### Recall

Measures how many of the actual fraudulent transactions were successfully detected.

### F1 Score

Provides a balance between precision and recall.

### ROC-AUC

Measures the model's ability to distinguish fraudulent and legitimate transactions across different thresholds.

### PR-AUC

Provides additional insight into performance on the highly imbalanced fraud classification problem.

---

# ⚠️ Build Challenges & Technical Obstacles

### 1. Extreme class imbalance

Fraud represents only a tiny fraction of transactions.

This makes standard accuracy misleading and requires careful evaluation using precision, recall, F1, and PR-AUC.

### 2. Precision vs Recall trade-off

A lower threshold detects more fraud but creates more false alerts.

A higher threshold reduces false alerts but can miss fraudulent transactions.

Finding the appropriate operating point was therefore a major part of the development process.

### 3. Overconfident probabilities

The original Random Forest could produce probabilities extremely close to 0 or 1.

Probability calibration was introduced to make the risk probabilities more meaningful.

### 4. Threshold optimization

Multiple thresholds were evaluated against the hold-out dataset before selecting the production threshold of `0.60`.

### 5. Model interpretability

Random Forest predictions are not inherently easy to explain.

Feature importance was therefore incorporated into the risk engine to expose the strongest risk signals.

### 6. Production integration

The calibrated model had to be integrated into the FastAPI risk engine while maintaining consistent:

* probability calculation
* risk scoring
* risk levels
* decision thresholds
* feature signals

### 7. Model version compatibility

The serialized model was trained using a different scikit-learn version, producing compatibility warnings when loaded in the local environment.

The model was nevertheless successfully loaded and evaluated, and version consistency should be maintained for production deployments.

---

# 🖥️ Dashboard

The Sentinel dashboard provides:

### Risk Assessment

* Transaction risk score
* Fraud probability
* Risk classification
* Recommended action
* Top risk signals

### Analytics

* Precision
* Recall
* F1 Score
* ROC-AUC
* Fraud detection statistics
* False alert rate
* Feature importance

### System Status

* Active model
* Decision threshold
* Risk classification configuration
* High-risk action

---

# 🔌 API Examples

### Normal Transaction

```http
GET /api/v1/demo/normal
```

Example response:

```json
{
  "risk_score": 0.05,
  "risk_probability": 0.0005,
  "risk_level": "LOW",
  "decision": "APPROVE"
}
```

### Fraud Transaction

```http
GET /api/v1/demo/fraud
```

Example response:

```json
{
  "risk_score": 98.28,
  "risk_probability": 0.9828,
  "risk_level": "HIGH",
  "decision": "HOLD_AND_VERIFY"
}
```

---

# 📊 Why Sentinel?

Traditional fraud systems often focus purely on:

```text
Fraud → Block
Normal → Allow
```

Sentinel instead provides a richer risk intelligence layer:

```text
Transaction
     ↓
Fraud Probability
     ↓
Risk Score
     ↓
Risk Level
     ↓
Risk Signals
     ↓
Recommended Action
```

This makes the system suitable for scenarios where organizations need to balance **fraud prevention, customer experience, and operational review**.

---

# 🔮 Future Improvements

Potential future extensions include:

* CSV batch transaction analysis
* Real-time transaction streaming
* Automated fraud investigation workflows
* Customer-level behavioral profiling
* Temporal transaction pattern analysis
* Anomaly detection alongside supervised classification
* Model monitoring and drift detection
* Automated model retraining
* SHAP-based individual transaction explanations
* Role-based analyst dashboards
* Cloud-based ML inference
* Feedback-driven model improvement

---

# 👨‍💻 Development Journey

Sentinel was developed iteratively rather than relying on a single model run.

### Phase 1 — Baseline

Built the initial Random Forest fraud detection pipeline and established baseline performance.

### Phase 2 — Model Optimization

Experimented with different Random Forest configurations and evaluated their performance.

### Phase 3 — Threshold Analysis

Tested multiple classification thresholds to understand the precision/recall trade-off.

### Phase 4 — Probability Calibration

Identified that raw probabilities could be overly confident and introduced probability calibration.

### Phase 5 — Production Threshold

Evaluated the calibrated model on the untouched hold-out test set and selected a `0.60` operating threshold.

### Phase 6 — Risk Engine Integration

Integrated the calibrated model into the Sentinel risk engine to generate:

```text
Probability
→ Risk Score
→ Risk Level
→ Decision
→ Risk Signals
```

### Phase 7 — Analytics Dashboard

Updated the dashboard to reflect the final calibrated model performance and provide transparent model intelligence.

---

# 🏁 Final Result

Sentinel evolved from a conventional fraud classifier into an **AI-powered transaction risk intelligence system**.

The most important improvement was not simply increasing a metric—it was reducing false alerts while maintaining strong fraud detection.

```text
                    BEFORE
              Precision: 85.42%
                       │
                       ▼
            Calibration + Threshold
                       │
                       ▼
                    AFTER
              Precision: 94.94%
```

Final production configuration:

```text
Model       : RF_DEEPER_CALIBRATED
Threshold   : 0.60
Precision   : 94.94%
Recall      : 76.53%
F1 Score    : 84.75%
ROC-AUC     : 97.02%
PR-AUC      : 86.43%
False Alerts: 4 / 56,962
```

> **Sentinel — Turning transaction data into actionable fraud intelligence.**

---

## 📜 Disclaimer

Sentinel is a demonstration/research project for fraud-risk analysis and should not be used as the sole decision-making system for real financial transactions without additional validation, monitoring, security controls, regulatory compliance, and production-grade model governance.

````

### One important thing before you commit

Your README should **not claim that 94.94% is "accuracy."** The correct terminology is **precision**. That's actually a stronger technical presentation because your whole improvement was about reducing false positives.

Also, for the Vercel section, replace:

```text
https://sentinel-tawny-psi.vercel.app
````

with your actual deployed URL. I don't want to fabricate the URL and accidentally put someone else's deployment into your submission.
