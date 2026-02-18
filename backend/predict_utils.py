import joblib
import pandas as pd

# -----------------------------
# LOAD MODEL & ENCODERS (ONCE)
# -----------------------------
model = joblib.load("funding_model.pkl")
encoders = joblib.load("label_encoders.pkl")

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

# =====================================================
# MAIN PREDICTION FUNCTION (FOR FASTAPI)
# =====================================================
def predict(payload: dict):

    # -----------------------------
    # READ INPUTS (SAME NAMES)
    # -----------------------------
    user_type = payload["panel"].strip().lower()

    industry = payload["industry"]
    city = payload["city"]
    founded_year = payload["founded_year"]
    no_of_founders = payload["no_of_founders"]
    funding_stage = payload["funding_stage"]
    previous_funding_amount = payload["previous_funding_amount"]
    investment_type = payload["investment_type"]
    market_size_category = payload["market_size_category"]

    # -----------------------------
    # FEATURE ENGINEERING (UNCHANGED)
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
    # SAFE ENCODING (UNCHANGED)
    # -----------------------------
    for col, le in encoders.items():
        if col in input_df.columns:
            matched_value = match_encoder_value(input_df[col].iloc[0], le)
            input_df[col] = le.transform([matched_value])

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
    # BASE JSON OUTPUT (SAME STRUCTURE)
    # -----------------------------
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

    # -----------------------------
    # FOUNDER PANEL OUTPUT (UNCHANGED)
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

        json_output["founder_outputs"] = {
            "funding_readiness": readiness,
            "insight": insight
        }

    # -----------------------------
    # INVESTOR PANEL OUTPUT (UNCHANGED)
    # -----------------------------
    if user_type == "investor":
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

        json_output["investor_outputs"] = {
            "investment_score": score,
            "risk_level": risk,
            "decision": decision
        }

    return json_output
