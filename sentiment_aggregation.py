import pandas as pd
import numpy as np

# --------------------------------------------------
# Config
# --------------------------------------------------
INPUT_FILE = "data/news_day2_sentiment.csv"
OUTPUT_FILE = "data/news_day3_company_state.csv"

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv(INPUT_FILE)

required_cols = [
    "company",
    "sentiment_label",
    "sentiment_score"
]

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

print(f"Loaded {len(df)} sentiment-scored articles")

# --------------------------------------------------
# Aggregation logic
# --------------------------------------------------
company_states = []

for company, group in df.groupby("company"):
    total = len(group)

    pos = (group["sentiment_label"] == "positive").sum()
    neg = (group["sentiment_label"] == "negative").sum()
    neu = (group["sentiment_label"] == "neutral").sum()

    pos_pct = round(pos / total, 3)
    neg_pct = round(neg / total, 3)
    neu_pct = round(neu / total, 3)

    avg_score = round(group["sentiment_score"].mean(), 3)

    # --------------------------------------------------
    # Define sentiment state (simple & explainable)
    # --------------------------------------------------
    if neg_pct >= 0.25:
        sentiment_state = "negative_bias"
    elif pos_pct >= 0.25:
        sentiment_state = "positive_bias"
    elif neu_pct >= 0.7:
        sentiment_state = "neutral_stable"
    else:
        sentiment_state = "mixed_uncertain"

    company_states.append({
        "company": company,
        "total_articles": total,
        "positive_pct": pos_pct,
        "negative_pct": neg_pct,
        "neutral_pct": neu_pct,
        "avg_sentiment_score": avg_score,
        "sentiment_state": sentiment_state
    })

# --------------------------------------------------
# Save output
# --------------------------------------------------
final_df = pd.DataFrame(company_states)
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved company-level sentiment state → {OUTPUT_FILE}")
print(final_df[["company", "sentiment_state", "total_articles"]])
