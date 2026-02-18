import { useState } from "react";
import PanelSelector from "./components/PanelSelector";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import { getPrediction } from "./services/api";
import "./App.css";

function App() {
  const [panel, setPanel] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (data) => {
    const response = await getPrediction(data);
    setResult(response);
  };

  return (
    <div className="container">
      <h1>Funding Analysis</h1>

      <PanelSelector panel={panel} setPanel={setPanel} />

      {panel && <InputForm panel={panel} onSubmit={handleSubmit} />}

      <ResultCard result={result} />
    </div>
  );
}

export default App;
