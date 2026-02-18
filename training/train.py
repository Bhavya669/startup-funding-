import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -----------------------------
# LOAD FEATURE ENGINEERED DATA
# -----------------------------
df = pd.read_csv("feature_engineered_data.csv")

print("Data loaded")
print("Shape:", df.shape)

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

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# DECISION TREE
# -----------------------------
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
dt_acc = accuracy_score(y_test, dt.predict(X_test))

print("Decision Tree Accuracy:", round(dt_acc * 100, 2), "%")

# -----------------------------
# RANDOM FOREST
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
rf.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf.predict(X_test))

print("Random Forest Accuracy:", round(rf_acc * 100, 2), "%")

# -----------------------------
# BEST MODEL
# -----------------------------
best_model = "Random Forest" if rf_acc > dt_acc else "Decision Tree"

print("\nBest Model:", best_model)
print("Model training completed")
