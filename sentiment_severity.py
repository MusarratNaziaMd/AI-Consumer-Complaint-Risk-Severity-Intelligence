# sentiment_severity_chunked.py

import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os

# ------------------ SETUP ------------------
nltk.download('vader_lexicon')

INPUT_CSV = "data/cleaned_complaints.csv"
OUTPUT_CSV = "data/processed_complaints.csv"
VISUALS_DIR = "visuals"

os.makedirs(VISUALS_DIR, exist_ok=True)

# ------------------ LOAD DATA ------------------
print("Loading data...")
df = pd.read_csv(INPUT_CSV)
print(f"Total rows loaded: {len(df)}")

# Handle missing columns safely
if "Issue" not in df.columns:
    df["Issue"] = ""

if "Product" not in df.columns:
    raise ValueError("❌ Product column missing in dataset")

# ------------------ NLP INIT ------------------
sia = SentimentIntensityAnalyzer()

# ------------------ FUNCTIONS ------------------
def get_sentiment(text):
    score = sia.polarity_scores(str(text))["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    return "Neutral"

def assign_severity(row):
    issue = str(row["Issue"]).lower()
    sentiment = row["Sentiment"]
    product = str(row["Product"]).lower()

    high_risk_keywords = [
        "fraud", "scam", "identity",
        "unauthorized", "harassment",
        "charge", "dispute"
    ]

    high_risk_products = [
        "credit card",
        "debt collection",
        "mortgage",
        "student loan"
    ]

    if sentiment == "Negative" and (
        any(k in issue for k in high_risk_keywords)
        or any(p in product for p in high_risk_products)
    ):
        return "High"

    if sentiment == "Negative":
        return "Medium"

    return "Low"

# ------------------ BATCH PROCESSING ------------------
batch_size = 50000
processed_chunks = []

for start in range(0, len(df), batch_size):
    end = min(start + batch_size, len(df))
    print(f"Processing rows {start} → {end}")

    batch = df.iloc[start:end].copy()
    batch["Sentiment"] = batch["Consumer complaint narrative"].apply(get_sentiment)
    batch["Severity"] = batch.apply(assign_severity, axis=1)

    processed_chunks.append(batch)

df_processed = pd.concat(processed_chunks, ignore_index=True)
print("Processing complete.")

# ------------------ SAVE OUTPUT ------------------
df_processed.to_csv(OUTPUT_CSV, index=False)
print(f"Processed file saved → {OUTPUT_CSV}")

# ------------------ ANALYTICS ------------------
severity_counts = df_processed["Severity"].value_counts()

high_df = df_processed[df_processed["Severity"] == "High"]

top_risk_product = (
    high_df["Product"].value_counts().idxmax()
    if not high_df.empty else "N/A"
)

print("Severity counts:")
print(severity_counts)
print(f"Top risk product: {top_risk_product}")

# ------------------ VISUAL 1: SEVERITY PIE ------------------
plt.figure(figsize=(6, 6))
severity_counts.plot.pie(
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Complaint Severity Distribution")
plt.ylabel("")
plt.tight_layout()

plt.savefig(f"{VISUALS_DIR}/severity_distribution.png")
plt.close()

# ------------------ VISUAL 2: HIGH RISK PRODUCTS ------------------
if not high_df.empty:
    high_df["Product"].value_counts().head(5).plot(
        kind="bar",
        title="Top High-Risk Products",
        ylabel="Number of Complaints"
    )
    plt.tight_layout()
    plt.savefig(f"{VISUALS_DIR}/high_risk_products.png")
    plt.close()

print("All visuals generated successfully ✅")
print("DONE 🚀")
