import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# --------------------------------------------------
# Config
# --------------------------------------------------
INPUT_FILE = "data/news_day1_final.csv"
OUTPUT_FILE = "data/news_day2_sentiment.csv"

TEXT_COLUMN = "content"

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv(INPUT_FILE)

if df.empty:
    raise ValueError("Input dataset is empty. Check Day 1 output.")

print(f"Loaded {len(df)} articles")

# --------------------------------------------------
# Load FinBERT sentiment pipeline
# --------------------------------------------------
sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    truncation=True
)

# --------------------------------------------------
# Run sentiment analysis
# --------------------------------------------------
sentiment_labels = []
sentiment_scores = []

print("Running FinBERT sentiment analysis...")

for text in tqdm(df[TEXT_COLUMN], total=len(df)):
    try:
        result = sentiment_model(text[:512])[0]
        sentiment_labels.append(result["label"].lower())
        sentiment_scores.append(result["score"])
    except Exception:
        sentiment_labels.append("neutral")
        sentiment_scores.append(0.0)

# --------------------------------------------------
# Append results
# --------------------------------------------------
df["sentiment_label"] = sentiment_labels
df["sentiment_score"] = sentiment_scores

# --------------------------------------------------
# Save output
# --------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved sentiment-enriched dataset → {OUTPUT_FILE}")
print(df["sentiment_label"].value_counts())
 