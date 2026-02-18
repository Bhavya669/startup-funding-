import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# LOAD CLEANED DATA
# -----------------------------
df = pd.read_csv("cleaned_startup_data.csv")

print("EDA started")
print("Dataset shape:", df.shape)

# -----------------------------
# BASIC OVERVIEW
# -----------------------------
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())

# -----------------------------
# TARGET DISTRIBUTION
# -----------------------------
plt.figure()
df["target_funding_category"].value_counts().plot(kind="bar")
plt.title("Target Funding Category Distribution")
plt.xlabel("Funding Category")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("target_distribution.png")
plt.show()

# -----------------------------
# FUNDING BY INDUSTRY
# -----------------------------
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="industry", hue="target_funding_category")
plt.title("Funding Category by Industry")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("industry_vs_funding.png")
plt.show()

# -----------------------------
# FUNDING BY CITY
# -----------------------------
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="city", hue="target_funding_category")
plt.title("Funding Category by City")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("city_vs_funding.png")
plt.show()

# -----------------------------
# NUMERIC DISTRIBUTIONS
# -----------------------------
numeric_cols = [
    "startup_age",
    "no_of_founders",
    "previous_funding_amount"
]

for col in numeric_cols:
    plt.figure()
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.tight_layout()
    plt.savefig(f"{col}_distribution.png")
    plt.show()

# -----------------------------
# NUMERIC VS TARGET
# -----------------------------
for col in numeric_cols:
    plt.figure()
    sns.boxplot(x="target_funding_category", y=col, data=df)
    plt.title(f"{col} vs Funding Category")
    plt.tight_layout()
    plt.savefig(f"{col}_vs_target.png")
    plt.show()

print("\nEDA completed successfully")
print("Plots saved in project folder")
