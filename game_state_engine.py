import pandas as pd

# --------------------------------------------------
# Config
# --------------------------------------------------
INPUT_FILE = "data/news_day3_company_state.csv"
OUTPUT_FILE = "data/news_day3_game_state.csv"

# --------------------------------------------------
# Load company sentiment states
# --------------------------------------------------
df = pd.read_csv(INPUT_FILE)

required_cols = ["company", "sentiment_state", "total_articles"]

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

print(f"Loaded {len(df)} company sentiment states")

# --------------------------------------------------
# Game state mapping logic
# --------------------------------------------------
game_states = []

for _, row in df.iterrows():
    company = row["company"]
    sentiment_state = row["sentiment_state"]
    volume = row["total_articles"]

    # -------------------------------
    # Define game state
    # -------------------------------
    if sentiment_state == "negative_bias":
        game_state = "defensive_risk"
        info_asymmetry = "high"

    elif sentiment_state == "positive_bias":
        game_state = "expansion_opportunity"
        info_asymmetry = "medium"

    elif sentiment_state == "neutral_stable":
        if volume >= 30:
            game_state = "wait_and_watch"
            info_asymmetry = "low"
        else:
            game_state = "range_bound"
            info_asymmetry = "medium"

    else:  # mixed_uncertain
        game_state = "strategic_uncertainty"
        info_asymmetry = "high"

    game_states.append({
        "company": company,
        "sentiment_state": sentiment_state,
        "game_state": game_state,
        "information_asymmetry": info_asymmetry
    })

# --------------------------------------------------
# Save output
# --------------------------------------------------
final_df = pd.DataFrame(game_states)
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved game state mapping → {OUTPUT_FILE}")
print(final_df)
