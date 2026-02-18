import pandas as pd

# -----------------------------
# LOAD ORIGINAL DATA
# -----------------------------
df = pd.read_excel("startup data.xlsx")

print("Original data loaded")
print("Shape:", df.shape)

# -----------------------------
# REMOVE DUPLICATES
# -----------------------------
df = df.drop_duplicates()
print("After removing duplicates:", df.shape)

# -----------------------------
# STANDARDIZE TEXT COLUMNS
# -----------------------------
text_cols = [
    "industry",
    "city",
    "funding_stage",
    "investment_type",
    "market_size_category",
    "target_funding_category"
]

for col in text_cols:
    df[col] = df[col].str.strip().str.title()

print("Text columns standardized")

# -----------------------------
# VALIDATE NUMERIC COLUMNS
# -----------------------------
df = df[df["no_of_founders"] > 0]
df = df[df["previous_funding_amount"] >= 0]

print("Numeric values validated")

# -----------------------------
# CREATE STARTUP AGE
# -----------------------------
CURRENT_YEAR = 2024
df["startup_age"] = CURRENT_YEAR - df["founded_year"]

print("Startup age created")

# -----------------------------
# FINAL CHECK
# -----------------------------
print("\nCleaned Data Info:")
print(df.info())

# -----------------------------
# SAVE CLEANED DATA
# -----------------------------
df.to_csv("cleaned_startup_data.csv", index=False)

print("\nData cleaning completed")
print("Saved as cleaned_startup_data.csv")
