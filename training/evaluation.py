import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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

for col in cat_cols:
    le = LabelEncoder()
    df_model[col] = le.fit_transform(df_model[col])

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
# TRAIN BEST MODEL (RF)
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# PREDICTION
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# CLASSIFICATION REPORT
# -----------------------------
print("\nCLASSIFICATION REPORT\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# CONFUSION MATRIX
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

print("\nModel evaluation completed")
