import { FaRupeeSign, FaLightbulb, FaExclamationTriangle } from "react-icons/fa";

function ResultCard({ result }) {
  if (!result) return null;

  return (
    <div className="result-card">
      <h3>Prediction Result</h3>

      <p><FaRupeeSign /> <b>{result.prediction.funding_category}</b></p>
      <p>Range: {result.prediction.funding_range}</p>

      {result.founder_outputs && (
        <p><FaLightbulb /> {result.founder_outputs.funding_readiness}</p>
      )}

      {result.investor_outputs && (
        <p><FaExclamationTriangle /> {result.investor_outputs.decision}</p>
      )}
    </div>
  );
}

export default ResultCard;
