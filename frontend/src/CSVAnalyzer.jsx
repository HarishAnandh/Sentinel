import { useState } from "react";
import "./CSVAnalyzer.css";

const API_URL = "http://127.0.0.1:8000";

function CSVAnalyzer() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setError("");
    setAnalysis(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please select a CSV file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const analyzeFile = async () => {
    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/api/v1/analyze/csv`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "CSV analysis failed."
        );
      }

      setAnalysis(data);
    } catch (err) {
      setError(err.message || "Unable to analyze CSV.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="csv-page">

      {/* HEADER */}

      <div className="csv-header">
        <div>
          <h1>CSV Risk Analysis</h1>
          <p>
            Upload transaction data and let Sentinel analyze
            every transaction using the calibrated fraud model.
          </p>
        </div>

        <span className="csv-online">
          ● MODEL ONLINE
        </span>
      </div>


      {/* UPLOAD CARD */}

      <div className="csv-upload-card">

        <div className="upload-icon">
          ↑
        </div>

        <h2>Upload Transaction CSV</h2>

        <p>
          Upload a CSV containing Time, V1–V28 and Amount.
        </p>

        <label className="csv-file-input">

          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
          />

          <span>
            {file
              ? file.name
              : "Choose CSV file"}
          </span>

        </label>

        {file && (
          <div className="selected-file">
            <span>Selected</span>
            <strong>{file.name}</strong>
          </div>
        )}

        <button
          className="analyze-button"
          onClick={analyzeFile}
          disabled={!file || loading}
        >
          {loading
            ? "Analyzing Transactions..."
            : "Analyze CSV"}
        </button>

        {error && (
          <div className="csv-error">
            {error}
          </div>
        )}

      </div>


      {/* RESULTS */}

      {analysis && (
        <>

          <div className="csv-results-header">
            <div>
              <h2>Analysis Results</h2>
              <p>
                {analysis.filename}
              </p>
            </div>

            <span className="analysis-complete">
              ANALYSIS COMPLETE
            </span>
          </div>


          {/* SUMMARY CARDS */}

          <div className="csv-metrics">

            <div className="csv-metric">
              <span>Total Transactions</span>
              <strong>
                {analysis.total_transactions.toLocaleString()}
              </strong>
            </div>

            <div className="csv-metric high">
              <span>High Risk</span>
              <strong>
                {analysis.high_risk}
              </strong>
            </div>

            <div className="csv-metric medium">
              <span>Medium Risk</span>
              <strong>
                {analysis.medium_risk}
              </strong>
            </div>

            <div className="csv-metric low">
              <span>Low Risk</span>
              <strong>
                {analysis.low_risk}
              </strong>
            </div>

            <div className="csv-metric alert">
              <span>Fraud Alerts</span>
              <strong>
                {analysis.fraud_alerts}
              </strong>
            </div>

            <div className="csv-metric">
              <span>Average Risk</span>
              <strong>
                {analysis.average_risk_score}
              </strong>
            </div>

          </div>


          {/* RESULTS TABLE */}

          <div className="csv-table-card">

            <div className="csv-table-header">
              <div>
                <h2>Transaction Risk Results</h2>
                <p>
                  Sentinel risk assessment for uploaded transactions
                </p>
              </div>
            </div>

            <div className="csv-table-wrapper">

              <table className="csv-table">

                <thead>
                  <tr>
                    <th>#</th>
                    <th>Time</th>
                    <th>Amount</th>
                    <th>Risk Score</th>
                    <th>Probability</th>
                    <th>Risk Level</th>
                    <th>Decision</th>
                  </tr>
                </thead>

                <tbody>

                  {analysis.results.map((transaction, index) => (

                    <tr key={index}>

                      <td>{index + 1}</td>

                      <td>
                        {Number(transaction.Time).toFixed(0)}
                      </td>

                      <td>
                        ₹{Number(transaction.Amount).toFixed(2)}
                      </td>

                      <td>
                        <strong>
                          {Number(
                            transaction.Risk_Score
                          ).toFixed(2)}
                        </strong>
                      </td>

                      <td>
                        {(Number(
                          transaction.Fraud_Probability
                        ) * 100).toFixed(2)}%
                      </td>

                      <td>
                        <span
                          className={`risk-badge ${transaction.Risk_Level.toLowerCase()}`}
                        >
                          {transaction.Risk_Level}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`decision-badge ${
                            transaction.Decision ===
                            "HOLD_AND_VERIFY"
                              ? "hold"
                              : "approve"
                          }`}
                        >
                          {transaction.Decision ===
                          "HOLD_AND_VERIFY"
                            ? "HOLD & VERIFY"
                            : "APPROVE"}
                        </span>
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </div>

        </>
      )}

    </section>
  );
}

export default CSVAnalyzer;