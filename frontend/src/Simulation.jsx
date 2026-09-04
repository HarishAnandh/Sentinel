
import React, { useState } from "react";
import "./Simulation.css";

const API = "https://sentinel1-wqdp.onrender.com";
function RiskRing({ score }) {
  const value = Number(score) || 0;

  let status = "LOW";

  if (value >= 70) {
    status = "HIGH";
  } else if (value >= 30) {
    status = "MEDIUM";
  }

  return (
    <div
      className={`risk-ring ${status.toLowerCase()}`}
      style={{
        "--risk-progress": `${value * 3.6}deg`,
      }}
    >
      <div className="risk-ring-inner">
        <strong>{value.toFixed(2)}</strong>
        <span>/ 100</span>
        <small>{status} RISK</small>
      </div>
    </div>
  );
}
function Simulation() {
  const [form, setForm] = useState({
    amount: "",
    time: "",
    device_status: "existing",
    transaction_frequency: 1,
    unusual_time: false,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const merchantSettings = JSON.parse(
    localStorage.getItem("sentinelMerchantSettings") || "{}"
  );
  
  const merchantAlertsEnabled =
    merchantSettings.alertsEnabled !== false &&
    merchantSettings.highRiskAlerts !== false;
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const analyzeTransaction = async () => {
    if (!form.amount || !form.time) {
      setResult({
        error: "Please enter the transaction amount and time.",
      });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API}/api/v1/simulation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          amount: Number(form.amount),
          time: Number(form.time),
          device_status: form.device_status,
          transaction_frequency: Number(form.transaction_frequency),
          unusual_time: form.unusual_time,
        }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error("Simulation error:", error);

      setResult({
        error:
          "Unable to connect to Sentinel backend. Please make sure the API is running.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="simulation-page">

      <div className="simulation-header">
        <h1>Transaction Simulation</h1>
        <p>
          Simulate a transaction and evaluate its fraud risk using Sentinel AI.
        </p>
      </div>

      <div className="simulation-card">

        <div className="input-group">
          <label>Transaction Amount</label>

          <input
            type="number"
            name="amount"
            placeholder="Enter transaction amount"
            value={form.amount}
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <label>Transaction Time</label>

          <input
            type="number"
            name="time"
            placeholder="Example: 82000"
            value={form.time}
            onChange={handleChange}
          />

          <small>
            Use the dataset time format. Example: 82000.
          </small>
        </div>

        <div className="input-group">
          <label>Device Status</label>

          <select
            name="device_status"
            value={form.device_status}
            onChange={handleChange}
          >
            <option value="existing">Existing Device</option>
            <option value="new">New Device</option>
          </select>
        </div>

        <div className="input-group">
          <label>Transactions in Recent Period</label>

          <input
            type="number"
            name="transaction_frequency"
            min="1"
            value={form.transaction_frequency}
            onChange={handleChange}
          />
        </div>

        <div className="checkbox-group">
          <input
            type="checkbox"
            id="unusual_time"
            name="unusual_time"
            checked={form.unusual_time}
            onChange={handleChange}
          />

          <label htmlFor="unusual_time">
            Transaction occurred at an unusual time
          </label>
        </div>

        <button
          className="analyze-button"
          onClick={analyzeTransaction}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Transaction"}
        </button>

      </div>

      {result && !result.error && (
        <div className="simulation-result">

          <h2>Sentinel AI Analysis</h2>

          <div className="risk-score-section">
            <h3>AI Risk Assessment</h3>

            <RiskRing
              score={result.risk?.risk_score}
            />

            <div className="risk-summary">
              <p>
                <strong>Decision:</strong>{" "}
                {result.risk?.decision}
              </p>

              <p>
                <strong>Fraud Probability:</strong>{" "}
                {result.risk?.risk_probability}
              </p>
            </div>
          </div>

          <div className="risk-info">

            <p>
              <strong>Risk Level:</strong>{" "}
              {result.risk?.risk_level ?? "Unknown"}
            </p>

            <p>
              <strong>Decision:</strong>{" "}
              {result.risk?.decision ?? "Unknown"}
            </p>

            <p>
              <strong>Fraud Probability:</strong>{" "}
              {result.risk?.risk_probability ?? "Unknown"}
            </p>

          </div>
          {result.risk?.risk_level === "HIGH" &&
              merchantAlertsEnabled && (
                <div className="merchant-alert">

                  <div className="merchant-alert-icon">
                    !
                  </div>

                  <div className="merchant-alert-content">
                    <strong>High-Risk Transaction Detected</strong>

                    <p>
                      Sentinel recommends holding this transaction for merchant
                      verification.
                      {merchantSettings.businessName && (
                        <>
                          {" "}
                          Alert generated for{" "}
                          <strong>{merchantSettings.businessName}</strong>.
                        </>
                      )}
                    </p>

                    <div className="merchant-alert-details">
                      <span>
                        Risk Score:{" "}
                        <strong>
                          {Number(result.risk?.risk_score || 0).toFixed(2)}
                        </strong>
                      </span>
                      {merchantSettings.email && (
                        <div className="merchant-alert-recipient">
                          Alert recipient: {merchantSettings.email}
                        </div>
                      )}

                      <span>
                        Decision:{" "}
                        <strong>
                          {result.risk?.decision === "HOLD_AND_VERIFY"
                            ? "HOLD & VERIFY"
                            : result.risk?.decision}
                        </strong>
                      </span>
                    </div>
                  </div>

                </div>
              )}
          {result.risk?.signals?.length > 0 && (
            <div className="signals">

              <h3>Risk Signals</h3>

              {result.risk.signals.map((signal, index) => (
                <div className="signal" key={index}>

                  <strong>
                    {signal.feature}
                  </strong>

                  <span>
                    {signal.severity}
                  </span>

                </div>
              ))}

            </div>
          )}

        </div>
      )}

      {result?.error && (
        <div className="simulation-error">
          {result.error}
        </div>
      )}

    </div>
  );
}

export default Simulation;

