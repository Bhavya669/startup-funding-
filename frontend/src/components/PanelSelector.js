import { FaUserTie, FaChartLine } from "react-icons/fa";

function PanelSelector({ panel, setPanel }) {
  return (
    <div className="panel-selector">
      <button
        className={panel === "founder" ? "active" : ""}
        onClick={() => setPanel("founder")}
      >
        <FaUserTie /> Founder
      </button>

      <button
        className={panel === "investor" ? "active" : ""}
        onClick={() => setPanel("investor")}
      >
        <FaChartLine /> Investor
      </button>
    </div>
  );
}

export default PanelSelector;
