import joblib
import pandas as pd
import json   # ✅ ADDED ONLY

# -----------------------------
# LOAD MODEL & ENCODERS
# -----------------------------
model = joblib.load("funding_model.pkl")
encoders = joblib.load("label_encoders.pkl")

print("Model and encoders loaded successfully")

# -----------------------------
# FEATURE ORDER (MUST MATCH TRAINING)
# -----------------------------
FEATURE_ORDER = [
    "industry",
    "founded_year",
    "city",
    "no_of_founders",
    "funding_stage",
    "previous_funding_amount",
    "investment_type",
    "market_size_category",
    "startup_age",
    "founder_strength",
    "funding_momentum",
    "funding_intensity"
]

# -----------------------------
# HELPER: SAFE VALUE MATCHING
# -----------------------------
def match_encoder_value(user_value, encoder):
    user_value = user_value.strip().lower()
    for val in encoder.classes_:
        if val.lower() == user_value:
            return val
    raise ValueError(f"Invalid input '{user_value}'. Allowed values: {list(encoder.classes_)}")

# -----------------------------
# SELECT USER TYPE
# -----------------------------
user_type = input("Select panel (Founder / Investor): ").strip().lower()

if user_type not in ["founder", "investor"]:
    print("Invalid panel selection. Choose Founder or Investor.")
    exit()

# -----------------------------
# TAKE INPUTS
# -----------------------------
print("\nEnter startup details:")

industry = input("Industry (e.g., SaaS, AI, EdTech): ")
city = input("City (e.g., Bangalore, Delhi): ")
founded_year = int(input("Founded year: "))
no_of_founders = int(input("Number of founders: "))
funding_stage = input("Funding stage (Seed / Series A / Series B): ")
previous_funding_amount = float(input("Previous funding amount: "))
investment_type = input("Investment type (Angel / VC): ")
market_size_category = input("Market size category (Small / Medium / Large): ")

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
CURRENT_YEAR = 2024
startup_age = CURRENT_YEAR - founded_year
founder_strength = no_of_founders * 10
funding_momentum = previous_funding_amount / (startup_age + 1)
funding_intensity = previous_funding_amount * startup_age

# -----------------------------
# CREATE INPUT DATAFRAME
# -----------------------------
input_df = pd.DataFrame([{
    "industry": industry,
    "founded_year": founded_year,
    "city": city,
    "no_of_founders": no_of_founders,
    "funding_stage": funding_stage,
    "previous_funding_amount": previous_funding_amount,
    "investment_type": investment_type,
    "market_size_category": market_size_category,
    "startup_age": startup_age,
    "founder_strength": founder_strength,
    "funding_momentum": funding_momentum,
    "funding_intensity": funding_intensity
}])

# -----------------------------
# SAFE ENCODING (CASE-INSENSITIVE)
# -----------------------------
for col, le in encoders.items():
    if col in input_df.columns:
        try:
            matched_value = match_encoder_value(input_df[col].iloc[0], le)
            input_df[col] = le.transform([matched_value])
        except ValueError as e:
            print("\nERROR:", e)
            exit()

# -----------------------------
# FORCE FEATURE ORDER
# -----------------------------
input_df = input_df[FEATURE_ORDER]

# -----------------------------
# MODEL PREDICTION
# -----------------------------
prediction = model.predict(input_df)[0]

label_map = {
    0: "Small Funding",
    1: "Medium Funding",
    2: "Large Funding"
}

predicted_label = label_map[prediction]

# -----------------------------
# COMMON DERIVED OUTPUTS
# -----------------------------
funding_range_map = {
    0: "₹0 – ₹5 Cr",
    1: "₹5 Cr – ₹12 Cr",
    2: "₹12 Cr+"
}

estimated_range = funding_range_map[prediction]

# -----------------------------
# FOUNDER PANEL OUTPUT
# -----------------------------
if user_type == "founder":

    if prediction == 0:
        readiness = "Low funding readiness. Focus on traction and validation."
    elif prediction == 1:
        readiness = "Moderate funding readiness. Improve metrics to scale."
    else:
        readiness = "High funding readiness. Strong investment potential."

    insight = (
        f"Startups in {industry.title()} from {city.title()} "
        f"at {funding_stage.title()} show higher funding success."
    )

    print("\n========== FOUNDER PANEL ==========")
    print("Predicted Funding Category:", predicted_label)
    print("Estimated Funding Range:", estimated_range)
    print("Funding Readiness:", readiness)
    print("Insight:", insight)
    print("==================================")

# -----------------------------
# INVESTOR PANEL OUTPUT
# -----------------------------
else:
    score = 5
    if prediction == 2:
        score += 3
    elif prediction == 1:
        score += 2
    if no_of_founders >= 3:
        score += 1
    if funding_stage.lower() in ["series a", "series b"]:
        score += 1

    score = min(score, 10)

    if prediction == 0:
        risk = "High Risk"
        decision = "Monitor Only"
    elif prediction == 1:
        risk = "Medium Risk"
        decision = "Recommended for Due Diligence"
    else:
        risk = "Low Risk"
        decision = "Recommended for Investment"

    print("\n========== INVESTOR PANEL ==========")
    print("Predicted Funding Category:", predicted_label)
    print("Investment Attractiveness Score:", score, "/ 10")
    print("Risk Level:", risk)
    print("Decision:", decision)
    print("===================================")

# ======================================================
# JSON OUTPUT (ADDED ONLY – NO LOGIC CHANGE ABOVE)
# ======================================================
json_output = {
    "panel": user_type,
    "inputs": {
        "industry": industry,
        "city": city,
        "founded_year": founded_year,
        "no_of_founders": no_of_founders,
        "funding_stage": funding_stage,
        "previous_funding_amount": previous_funding_amount,
        "investment_type": investment_type,
        "market_size_category": market_size_category
    },
    "prediction": {
        "funding_category": predicted_label,
        "funding_range": estimated_range
    }
}

if user_type == "founder":
    json_output["founder_outputs"] = {
        "funding_readiness": readiness,
        "insight": insight
    }

if user_type == "investor":
    json_output["investor_outputs"] = {
        "investment_score": score,
        "risk_level": risk,
        "decision": decision
    }

print("\n========== JSON OUTPUT ==========")
print(json.dumps(json_output, indent=4))
print("================================")
