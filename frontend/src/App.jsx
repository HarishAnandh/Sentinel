import { useEffect, useState } from "react";

import {
  ShieldCheck,
  LayoutDashboard,
  CreditCard,
  AlertTriangle,
  BarChart3,
  Settings,
  Search,
  RefreshCw,
  CheckCircle2,
  Clock3
} from "lucide-react";

import "./index.css";

const API = "https://sentinel1-wqdp.onrender.com";


function App() {

  const [transactions, setTransactions] = useState(() => {
    try {
      const saved = localStorage.getItem("sentinel_transactions");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);
  const [activePage, setActivePage] = useState("dashboard");

  useEffect(() => {
    localStorage.setItem(
      "sentinel_transactions",
      JSON.stringify(transactions)
    );
  }, [transactions]);
  

  // ==========================================
  // LOAD DEMO TRANSACTION
  // ==========================================

  async function loadTransaction(type) {

    setLoading(true);

    try {

      const response = await fetch(
        `${API}/api/v1/demo/${type}`
      );

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      const transaction = {

        id:
          "TXN-" +
          Math.floor(
            10000 + Math.random() * 90000
          ),

        amount: data.transaction.Amount,

        scenario: data.scenario,

        ...data.risk

      };

      setTransactions(previous => [
        transaction,
        ...previous
      ]);

      setSelected(transaction);

    } catch (error) {

      console.error("API error:", error);

    } finally {

      setLoading(false);

    }
  }


  // ==========================================
  // INITIAL TRANSACTION
  // ==========================================

  useEffect(() => {

    loadTransaction("normal");

  }, []);


  // ==========================================
  // DASHBOARD COUNTERS
  // ==========================================

  const total = transactions.length;

  const alerts = transactions.filter(
    transaction => transaction.risk_level !== "LOW"
  ).length;
  
  const held = transactions.filter(
    transaction => transaction.decision === "HOLD_AND_VERIFY"
  ).length;

  
  
  const fraudDetected = transactions.filter(
    transaction => transaction.scenario === "FRAUD"
  ).length;
  
  const approved = transactions.filter(
    transaction => transaction.decision === "APPROVE"
  ).length;
  
  const highRisk = transactions.filter(
    transaction => transaction.risk_level === "HIGH"
  ).length;
  
  const averageRisk =
    total > 0
      ? (
          transactions.reduce(
            (sum, transaction) =>
              sum + Number(transaction.risk_score || 0),
            0
          ) / total
        ).toFixed(1)
      : "0.0";

      const lowRisk = transactions.filter(
        transaction => transaction.risk_level === "LOW"
      ).length;
      
      const mediumRisk = transactions.filter(
        transaction => transaction.risk_level === "MEDIUM"
      ).length;
      
      const highRiskCount = transactions.filter(
        transaction => transaction.risk_level === "HIGH"
      ).length;
      
      const riskPercentage = count => {
        if (total === 0) return 0;
        return Math.round((count / total) * 100);
      };


  return (

    <div className="app">

      {/* =====================================
          SIDEBAR
      ====================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            <ShieldCheck size={22} />
          </div>

          <div>

            <div className="brand-name">
              Sentinel
            </div>

            <div className="brand-subtitle">
              AI Risk Manager
            </div>

          </div>

        </div>


        <nav>

          <div className="nav-section">
            OVERVIEW
          </div>

          <div
              className={
                "nav-item " +
                (activePage === "dashboard" ? "active" : "")
              }
              onClick={() => setActivePage("dashboard")}
            >
              <LayoutDashboard size={18} />
              Dashboard
            </div>

            <div
              className={
                "nav-item " +
                (activePage === "transactions" ? "active" : "")
              }
              onClick={() => setActivePage("transactions")}
            >
              <CreditCard size={18} />
              Transactions
            </div>

            <div
              className={
                "nav-item " +
                (activePage === "queue" ? "active" : "")
              }
              onClick={() => setActivePage("queue")}
            >
              <AlertTriangle size={18} />
              Risk Queue
            </div>

            <div
              className="nav-item"
              onClick={() => setActivePage("analytics")}
            >
              <BarChart3 size={18} />
              Analytics
            </div>


          <div className="nav-section">
            SYSTEM
          </div>

          <div
            className="nav-item"
            onClick={() => setActivePage("settings")}
          >
            <Settings size={18} />
            Settings
          </div>

        </nav>


        <div className="model-status">

          <div className="status-dot"></div>

          <div>

            <strong>
              AI Engine Online
            </strong>

            <span>
              RF_DEEPER
            </span>

          </div>

        </div>

      </aside>


      {/* =====================================
          MAIN CONTENT
      ====================================== */}

     <main className="main">

        {/* HEADER */}
        
        <header className="topbar">

          <div>

            <h1>
              Risk Overview
            </h1>

            <p>
              Monitor and respond to transaction risk
            </p>

          </div>


          <div className="top-actions">

            <button className="icon-button">
              <Search size={19} />
            </button>

            <div className="merchant">

              <div className="avatar">
                M
              </div>

              <div>

                <strong>
                  Demo Merchant
                </strong>

                <span>
                  Merchant account
                </span>

              </div>

            </div>

          </div>

          </header>

          {activePage === "transactions" ? (
            <TransactionsPage
              transactions={transactions}
              onSelect={setSelected}
            />
          ) : activePage === "queue" ? (
            <RiskQueuePage
              transactions={transactions}
              onSelect={setSelected}
            />
          ) : activePage === "analytics" ? (
            <AnalyticsPage />
          ) : activePage === "settings" ? (
            <SettingsPage />
          ) : (
          <>
       {/* =====================================
        STAT CARDS
    ====================================== */}

    <section className="stats">
      <StatCard
        title="Transactions"
        value={total}
        icon={<CreditCard size={20} />}
      />

      <StatCard
        title="Risk Alerts"
        value={alerts}
        icon={<AlertTriangle size={20} />}
      />

      <StatCard
        title="Held for Verification"
        value={held}
        icon={<Clock3 size={20} />}
      />

      <StatCard
        title="Model Status"
        value="Online"
        icon={<ShieldCheck size={20} />}
        status
      />
    </section>


        {/* =====================================
            TRANSACTION SIMULATOR
        ====================================== */}

        <section className="demo-panel">

          <div>

            <h2>
              Transaction Simulator
            </h2>

            <p>
              Run a real transaction through Sentinel's
              fraud detection model.
            </p>

          </div>


          <div className="demo-buttons">

            <button
              className="button secondary"
              onClick={() =>
                loadTransaction("normal")
              }
              disabled={loading}
            >

              <CheckCircle2 size={17} />

              Normal Transaction

            </button>


            <button
              className="button danger"
              onClick={() =>
                loadTransaction("fraud")
              }
              disabled={loading}
            >

              <AlertTriangle size={17} />

              Fraud Scenario

            </button>


            <button
              className="refresh"
              onClick={() =>
                loadTransaction("normal")
              }
              disabled={loading}
            >

              <RefreshCw
                size={17}
                className={
                  loading ? "spin" : ""
                }
              />

            </button>

          </div>

        </section>


        {/* =====================================
            CONTENT
        ====================================== */}
        <section className="risk-distribution card">

<div className="card-header">
  <div>
    <h2>Risk Distribution</h2>
    <p>Current transaction risk profile</p>
  </div>

  <span className="live">● LIVE</span>
</div>

<div className="risk-distribution-content">

  <div className="risk-stat">
    <div className="risk-stat-top">
      <span className="risk-dot low"></span>
      <span>Low Risk</span>
      <strong>{lowRisk}</strong>
    </div>

    <div className="distribution-bar">
      <div
        className="distribution-fill low-fill"
        style={{
          width: `${riskPercentage(lowRisk)}%`
        }}
      />
    </div>

    <small>{riskPercentage(lowRisk)}% of transactions</small>
  </div>


  <div className="risk-stat">
    <div className="risk-stat-top">
      <span className="risk-dot medium"></span>
      <span>Medium Risk</span>
      <strong>{mediumRisk}</strong>
    </div>

    <div className="distribution-bar">
      <div
        className="distribution-fill medium-fill"
        style={{
          width: `${riskPercentage(mediumRisk)}%`
        }}
      />
    </div>

    <small>{riskPercentage(mediumRisk)}% of transactions</small>
  </div>


  <div className="risk-stat">
    <div className="risk-stat-top">
      <span className="risk-dot high"></span>
      <span>High Risk</span>
      <strong>{highRiskCount}</strong>
    </div>

    <div className="distribution-bar">
      <div
        className="distribution-fill high-fill"
        style={{
          width: `${riskPercentage(highRiskCount)}%`
        }}
      />
    </div>

    <small>{riskPercentage(highRiskCount)}% of transactions</small>
  </div>

</div>

</section>
        <div className="content-grid">

          {/* TRANSACTIONS */}

          <section className="transactions card">

            <div className="card-header">

              <div>

                <h2>
                  Recent Transactions
                </h2>

                <p>
                  Live model assessments
                </p>

              </div>

              <span className="live">
                ● LIVE
              </span>

            </div>


            {transactions.length === 0 ? (

              <div className="empty">
                No transactions yet.
              </div>

            ) : (

              <div className="transaction-list">

                {transactions.map(
                  transaction => (

                    <div
                      className={
                        "transaction " +
                        (
                          selected?.id ===
                          transaction.id
                            ? "selected"
                            : ""
                        )
                      }

                      key={transaction.id}

                      onClick={() =>
                        setSelected(transaction)
                      }
                    >

                      <div className="transaction-icon">

                        {transaction.risk_level ===
                        "HIGH" ? (

                          <AlertTriangle size={18} />

                        ) : (

                          <CheckCircle2 size={18} />

                        )}

                      </div>


                      <div className="transaction-info">

                        <strong>
                          {transaction.id}
                        </strong>

                        <span>
                          {transaction.scenario}
                        </span>

                      </div>


                      <div className="transaction-amount">

                        ₹
                        {Number(
                          transaction.amount
                        ).toLocaleString(
                          "en-IN",
                          {
                            minimumFractionDigits: 2
                          }
                        )}

                      </div>


                      <RiskBadge
                        level={
                          transaction.risk_level
                        }
                      />
                      <div className="transaction-score">
                        {Number(transaction.risk_score).toFixed(1)}
                      </div>

                      <div className="decision">

                        {transaction.decision
                          .replaceAll(
                            "_",
                            " "
                          )}

                      </div>

                    </div>

                  )
                )}

              </div>

            )}

          </section>


          {/* RISK ASSESSMENT */}

          <section className="risk-detail card">

            <div className="card-header">

              <div>

                <h2>
                  Risk Assessment
                </h2>

                <p>
                  Sentinel AI analysis
                </p>

              </div>

            </div>


            {selected ? (

              <>

                <div className="risk-score">

                  <div
                    className={
                      "score-ring " +
                      selected.risk_level
                        .toLowerCase()
                    }
                  >

                    <strong>
                      {selected.risk_score}
                    </strong>

                    <span>
                      / 100
                    </span>

                  </div>


                  <div>

                    <RiskBadge
                      level={
                        selected.risk_level
                      }
                    />

                    

                    <p className="probability">

                      Fraud probability{" "}

                      <strong>

                        {(
                          selected.risk_probability *
                          100
                        ).toFixed(2)}
                        %

                      </strong>

                    </p>

                  <div className="risk-context">
                    {selected.risk_level === "HIGH"
                      ? "Transaction requires immediate verification."
                      : selected.risk_level === "MEDIUM"
                      ? "Transaction requires additional review."
                      : "Transaction appears within normal risk range."}
                  </div>

                  </div>

                </div>


                <div className="decision-box">
                  <div className="decision-label">
                    <Clock3 size={15} />
                    <span>RECOMMENDED ACTION</span>
                  </div>

                  <strong>
                    {selected.decision.replaceAll("_", " ")}
                  </strong>

                  <p>
                    {selected.decision === "HOLD_AND_VERIFY"
                      ? "Payment should be temporarily held while the transaction is verified."
                      : selected.decision === "REVIEW"
                      ? "Transaction should be reviewed before final approval."
                      : "Transaction can proceed normally."}
                  </p>
                </div>


                <div className="explanation">

  <h3>
    Why Sentinel flagged this transaction
  </h3>

  <p>
    The Random Forest risk model identified
    transaction patterns associated with
    previously observed fraudulent activity.
  </p>


  <div className="signal-list">
  {selected.signals?.map((signal) => (
    <div className="signal" key={signal.feature}>
      <div className="signal-name">
        {signal.feature}
      </div>

      <div className="signal-bar">
        <div
          className="signal-fill"
          style={{
            width: `${Math.min(
              signal.importance * 500,
              100
            )}%`
          }}
        />
      </div>

      <span>
        {signal.importance >= 0.15
          ? "High impact"
          : signal.importance >= 0.08
          ? "Significant"
          : "Moderate"}
      </span>
    </div>
  ))}
</div>


  <div className="model-note">

    <ShieldCheck size={15} />

    <span>
      Explanation based on Sentinel's
      Random Forest feature importance.
    </span>

  </div>

</div>

              </>

            ) : (

              <div className="empty">
                Select a transaction.
              </div>

            )}

          </section>

        </div>
           </>
        )}
      </main>

    </div>
  );
}


/* ==========================================
   STAT CARD
========================================== */

function StatCard({
  title,
  value,
  icon,
  status
}) {

  return (

    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>

        <span>
          {title}
        </span>

        <strong
          className={
            status ? "online" : ""
          }
        >
          {value}
        </strong>

      </div>

    </div>
  );
}


/* ==========================================
   RISK BADGE
========================================== */

function RiskBadge({ level }) {

  return (

    <span
      className={
        "risk-badge " +
        level.toLowerCase()
      }
    >

      {level}

    </span>
  );
}

function TransactionsPage({ transactions, onSelect }) {
  return (
    <div className="page-content">

      <div className="page-heading">
        <div>
          <h1>Transactions</h1>
          <p>Monitor all transactions assessed by Sentinel AI</p>
        </div>

        <span className="live">● LIVE</span>
      </div>

      <section className="card transaction-table-card">

        <div className="table-summary">
          <div>
            <strong>{transactions.length}</strong>
            <span>Total transactions</span>
          </div>

          <div>
            <strong>
              {
                transactions.filter(
                  t => t.risk_level === "HIGH"
                ).length
              }
            </strong>
            <span>High risk</span>
          </div>

          <div>
            <strong>
              {
                transactions.filter(
                  t => t.decision === "HOLD_AND_VERIFY"
                ).length
              }
            </strong>
            <span>Held</span>
          </div>
        </div>

        {transactions.length === 0 ? (

          <div className="empty">
            No transactions available.
          </div>

        ) : (

          <div className="full-transaction-list">

            <div className="transaction-table-header">
              <span>TRANSACTION</span>
              <span>SCENARIO</span>
              <span>AMOUNT</span>
              <span>RISK</span>
              <span>SCORE</span>
              <span>DECISION</span>
            </div>

            {transactions.map(transaction => (

              <div
                className="transaction-table-row"
                key={transaction.id}
                onClick={() => onSelect(transaction)}
              >

                <div className="table-transaction-id">
                  <strong>{transaction.id}</strong>
                  <small>
                    {transaction.scenario === "FRAUD"
                      ? "Fraud scenario"
                      : "Normal transaction"}
                  </small>
                </div>

                <span>
                  {transaction.scenario}
                </span>

                <strong>
                  ₹
                  {Number(transaction.amount).toLocaleString(
                    "en-IN",
                    {
                      minimumFractionDigits: 2
                    }
                  )}
                </strong>

                <RiskBadge
                  level={transaction.risk_level}
                />

                <strong className="table-score">
                  {Number(transaction.risk_score).toFixed(1)}
                </strong>

                <span className="table-decision">
                  {transaction.decision.replaceAll(
                    "_",
                    " "
                  )}
                </span>

              </div>

            ))}

          </div>

        )}

      </section>

    </div>
  );
}
function RiskQueuePage({ transactions, onSelect }) {

  const riskTransactions = transactions.filter(
    transaction =>
      transaction.risk_level === "HIGH" ||
      transaction.decision === "HOLD_AND_VERIFY"
  );

  return (
    <section className="page">

      <div className="page-header">
        <div>
          <h1>Risk Queue</h1>
          <p>
            Transactions requiring verification
          </p>
        </div>

        <span className="live">
          ● LIVE
        </span>
      </div>

      <div className="card">

        <div className="card-header">

          <div>
            <h2>
              High Risk Transactions
            </h2>

            <p>
              Sentinel transactions awaiting review
            </p>
          </div>

          <strong>
            {riskTransactions.length} alerts
          </strong>

        </div>

        {riskTransactions.length === 0 ? (

          <div className="empty">
            No high-risk transactions currently in the queue.
          </div>

        ) : (

          <div className="transaction-list">

            {riskTransactions.map(transaction => (

              <div
                className="transaction"
                key={transaction.id}
                onClick={() => onSelect(transaction)}
              >

                <div className="transaction-icon">
                  <AlertTriangle size={18} />
                </div>

                <div className="transaction-info">

                  <strong>
                    {transaction.id}
                  </strong>

                  <span>
                    {transaction.scenario}
                  </span>

                </div>

                <div className="transaction-amount">

                  ₹
                  {Number(
                    transaction.amount
                  ).toLocaleString(
                    "en-IN",
                    {
                      minimumFractionDigits: 2
                    }
                  )}

                </div>

                <RiskBadge
                  level={transaction.risk_level}
                />

                <div className="decision">

                  {transaction.decision.replaceAll(
                    "_",
                    " "
                  )}

                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </section>
  );
}

function AnalyticsPage() {
  return (
    <section className="page">

      <div className="page-header">
        <div>
          <h1>Analytics</h1>
          <p>
            Sentinel model performance and risk intelligence
          </p>
        </div>

        <span className="live">
          ● MODEL ONLINE
        </span>
      </div>

      {/* MODEL PERFORMANCE */}

      <div className="analytics-grid">

        <div className="card analytics-card">
          <span>Precision</span>
          <strong>85.42%</strong>
          <small>Fraud detection accuracy</small>
        </div>

        <div className="card analytics-card">
          <span>Recall</span>
          <strong>83.67%</strong>
          <small>Fraud cases detected</small>
        </div>

        <div className="card analytics-card">
          <span>F1 Score</span>
          <strong>84.54%</strong>
          <small>Balanced model performance</small>
        </div>

        <div className="card analytics-card">
          <span>ROC-AUC</span>
          <strong>97.02%</strong>
          <small>Model discrimination</small>
        </div>

      </div>


      {/* MODEL INFORMATION */}

      <div className="card analytics-section">

        <div className="card-header">
          <div>
            <h2>Model Performance</h2>
            <p>
              Final hold-out test evaluation
            </p>
          </div>
        </div>

        <div className="model-metrics">

          <div>
            <span>Test transactions</span>
            <strong>56,962</strong>
          </div>

          <div>
            <span>Actual fraud cases</span>
            <strong>98</strong>
          </div>

          <div>
            <span>Fraud detected</span>
            <strong>82 / 98</strong>
          </div>

          <div>
            <span>False alerts</span>
            <strong>14</strong>
          </div>

          <div>
            <span>False alert rate</span>
            <strong>0.0246%</strong>
          </div>

          <div>
            <span>Active model</span>
            <strong>RF_DEEPER</strong>
          </div>

        </div>

      </div>


      {/* FEATURE IMPORTANCE */}

      <div className="card analytics-section">

        <div className="card-header">
          <div>
            <h2>Top Risk Signals</h2>
            <p>
              Random Forest feature importance
            </p>
          </div>
        </div>

        <div className="feature-bars">

          {[
            ["V14", 18.33],
            ["V10", 11.46],
            ["V4", 11.42],
            ["V12", 9.87],
            ["V17", 8.94]
          ].map(([feature, value]) => (

            <div className="feature-row" key={feature}>

              <div className="feature-label">
                <strong>{feature}</strong>
                <span>{value}%</span>
              </div>

              <div className="feature-bar">
                <div
                  className="feature-fill"
                  style={{
                    width: `${value * 5}%`
                  }}
                />
              </div>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}
function SettingsPage() {
  return (
    <section className="page">

      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p>
            Sentinel system and model configuration
          </p>
        </div>
      </div>

      <div className="card settings-card">

        <div className="card-header">
          <div>
            <h2>AI Risk Engine</h2>
            <p>
              Current fraud detection configuration
            </p>
          </div>

          <span className="status-badge">
            ONLINE
          </span>
        </div>

        <div className="settings-list">

          <div className="setting-row">
            <div>
              <strong>Active Model</strong>
              <span>Production fraud detection model</span>
            </div>

            <strong>RF_DEEPER</strong>
          </div>

          <div className="setting-row">
            <div>
              <strong>Decision Threshold</strong>
              <span>Probability threshold for fraud classification</span>
            </div>

            <strong>0.50</strong>
          </div>

          <div className="setting-row">
            <div>
              <strong>Risk Classification</strong>
              <span>LOW / MEDIUM / HIGH</span>
            </div>

            <strong>30 / 70</strong>
          </div>

          <div className="setting-row">
            <div>
              <strong>High Risk Action</strong>
              <span>Recommended action for high-risk transactions</span>
            </div>

            <strong>HOLD & VERIFY</strong>
          </div>

        </div>

      </div>

    </section>
  );
}
export default App;