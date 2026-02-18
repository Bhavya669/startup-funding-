import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("feature_engineered_data.csv")

# -----------------------------
# DROP DISPLAY-ONLY FEATURES
# -----------------------------
df_model = df.drop(columns=[
    "startup_maturity",
    "strong_team_flag"
])

# -----------------------------
# ENCODE CATEGORICAL COLUMNS
# -----------------------------
cat_cols = [
    "industry",
    "city",
    "funding_stage",
    "investment_type",
    "market_size_category",
    "target_funding_category"
]

encoders = {}

for col in cat_cols:
    le = LabelEncoder()
    df_model[col] = le.fit_transform(df_model[col])
    encoders[col] = le

# -----------------------------
# SPLIT FEATURES & TARGET
# -----------------------------
X = df_model.drop(columns=["target_funding_category"])
y = df_model["target_funding_category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# TRAIN FINAL MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# SAVE MODEL & ENCODERS
# -----------------------------
joblib.dump(model, "funding_model.pkl")
joblib.dump(encoders, "label_encoders.pkl")

print("Model saved as funding_model.pkl")
print("Encoders saved as label_encoders.pkl")
print("Model saving completed")
