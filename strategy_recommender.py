import pandas as pd

# --------------------------------------------------
# Config
# --------------------------------------------------
INPUT_FILE = "data/news_day3_game_state.csv"
OUTPUT_FILE = "data/news_day3_strategy.csv"

# --------------------------------------------------
# Load game states
# --------------------------------------------------
df = pd.read_csv(INPUT_FILE)

required_cols = ["company", "game_state", "information_asymmetry"]

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

print(f"Loaded {len(df)} company game states")

# --------------------------------------------------
# Strategy recommendation logic
# --------------------------------------------------
strategies = []

for _, row in df.iterrows():
    company = row["company"]
    game_state = row["game_state"]
    asymmetry = row["information_asymmetry"]

    # ----------------------------------------------
    # Strategy rules (game-theoretic, not predictive)
    # ----------------------------------------------
    if game_state == "defensive_risk":
        strategy = "avoid_or_hedge"
        rationale = (
            "Negative sentiment with high information asymmetry. "
            "Downside risk dominates without clear signals."
        )

    elif game_state == "expansion_opportunity":
        strategy = "accumulate_selectively"
        rationale = (
            "Positive sentiment suggests opportunity, but confirmation "
            "is required before aggressive positioning."
        )

    elif game_state == "range_bound":
        strategy = "tactical_hold"
        rationale = (
            "Mixed or low-conviction signals indicate sideways movement. "
            "Best response is patience and optionality."
        )

    elif game_state == "wait_and_watch":
        strategy = "hold_and_monitor"
        rationale = (
            "Stable sentiment and low asymmetry. "
            "No dominant catalyst; observation is optimal."
        )

    else:
        strategy = "no_clear_action"
        rationale = (
            "High uncertainty environment. "
            "Insufficient clarity for rational positioning."
        )

    strategies.append({
        "company": company,
        "game_state": game_state,
        "information_asymmetry": asymmetry,
        "recommended_strategy": strategy,
        "rationale": rationale
    })

# --------------------------------------------------
# Save output
# --------------------------------------------------
final_df = pd.DataFrame(strategies)
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved strategy recommendations → {OUTPUT_FILE}")
print(final_df)
