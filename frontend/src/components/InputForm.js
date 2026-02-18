import { useState } from "react";


function InputForm({ panel, onSubmit }) {
  const [data, setData] = useState({
    industry: "",
    city: "",
    founded_year: "",
    no_of_founders: "",
    funding_stage: "",
    previous_funding_amount: "",
    investment_type: "",
    market_size_category: ""
  });

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      panel,
      founded_year: Number(data.founded_year),
      no_of_founders: Number(data.no_of_founders),
      previous_funding_amount: Number(data.previous_funding_amount),
      ...data
    });
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h3>{panel === "founder" ? "Founder Inputs" : "Investor Inputs"}</h3>

      <select name="industry" onChange={handleChange} required>
        <option value="">Industry</option>
        <option value="saas">SaaS</option>
        <option value="ai">AI</option>
        <option value="edtech">EdTech</option>
        <option value="healthtech">HealthTech</option>
        <option value="ecommerce">E-Commerce</option>
        <option value="fintech">FinTech</option>
      </select>

      <select name="city" onChange={handleChange} required>
        <option value="">City</option>
        <option value="mumbai">Mumbai</option>
        <option value="delhi">Delhi</option>
        <option value="chennai">Chennai</option>
        <option value="pune">Pune</option>
        <option value="hyderabad">Hyderabad</option>
        <option value="bangalore">Bangalore</option>
      </select>

      <input name="founded_year" type="number" placeholder="Founded Year" onChange={handleChange} required />
      <input name="no_of_founders" type="number" placeholder="Number of Founders" onChange={handleChange} required />

      <select name="funding_stage" onChange={handleChange} required>
        <option value="">Funding Stage</option>
        <option value="seed">Seed</option>
        <option value="series a">Series A</option>
        <option value="series b">Series B</option>
      </select>

      <input
        name="previous_funding_amount"
        type="number"
        placeholder="Previous Funding Amount (₹ Cr)"
        onChange={handleChange}
        required
      />

      <select name="investment_type" onChange={handleChange} required>
        <option value="">Investment Type</option>
        <option value="angel">Angel</option>
        <option value="vc">VC</option>
        <option value="pe">PE</option>
      </select>

      <select name="market_size_category" onChange={handleChange} required>
        <option value="">Market Size</option>
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
      </select>

      <button type="submit">Get Funding Analysis</button>
    </form>
  );
}

export default InputForm;
