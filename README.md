Game Theory + Sentiment Analysis

Decision Support System — Proof of Concept (v1)

1. Project Overview

This repository contains PoC v1 of a decision support system that integrates:

Financial news sentiment analysis

Game-theoretic state modeling

Strategy recommendation under information asymmetry

The system does not attempt price prediction or alpha generation.
Instead, it focuses on decision context — identifying rational strategic postures based on how information evolves in public narratives.

This version prioritizes conceptual clarity, explainability, and modularity over sophistication and performance.

2. Core Idea

Most sentiment-based systems stop at classification (positive/negative/neutral).
This project goes one step further by asking:

Given the current sentiment environment, what is the rational response for a decision-maker?

Game theory provides a natural abstraction to model:

Uncertainty

Information asymmetry

Defensive vs opportunistic behavior

Stable vs volatile states

The output is a strategy-oriented recommendation, not a prediction.

3. End-to-End Pipeline
Raw News
   ↓
Sentiment Scoring (FinBERT)
   ↓
Company-Level Aggregation
   ↓
Game State Inference
   ↓
Strategy Recommendation
   ↓
Static HTML Dashboard


Each stage is implemented as an independent module, allowing future upgrades without refactoring the entire system.

4. Repository Structure
Game Theory + Sentiment Analysis/
│
├── data/
│   ├── news_raw.csv                 # Raw scraped news
│   ├── news_day1_final.csv          # Cleaned & filtered articles
│   ├── news_day2_sentiment.csv      # Article-level sentiment scores
│   ├── news_day3_company_state.csv  # Aggregated company sentiment states
│   ├── news_day3_game_state.csv     # Game-theoretic state mapping
│   ├── news_day3_strategy.csv       # Final strategy recommendations
│
├── config.py                        # Central configuration (companies, paths)
│
├── news_ingestion.py                # News scraping & ingestion
├── postprocess_tagging.py           # Cleaning & tagging logic
│
├── sentiment_engine.py              # FinBERT sentiment scoring
├── sentiment_aggregation.py         # Company-level aggregation
│
├── game_state_engine.py             # Game-theoretic state inference
├── strategy_recommender.py          # Strategy mapping logic
│
├── html_dashboard_generator.py      # Static HTML dashboard generation
├── dashboard.html                   # Final offline dashboard
│
├── test.py                          # Sanity checks / experiments
└── README.md

5. Module-Level Explanation
5.1 News Ingestion

news_ingestion.py

Scrapes publicly available financial news

Filters by company relevance

Outputs structured article data

Design choice:
Focus on robustness and transparency, not source volume.

5.2 Sentiment Analysis

sentiment_engine.py

Uses FinBERT (ProsusAI) for finance-specific sentiment

Produces:

sentiment label (positive / neutral / negative)

confidence score

This avoids generic NLP sentiment models that perform poorly on financial text.

5.3 Sentiment Aggregation

sentiment_aggregation.py

Aggregates article-level sentiment to company-level states

Reduces noise and overreaction to single headlines

Example outputs:

neutral_stable

negative_bias

5.4 Game State Modeling

game_state_engine.py

Maps sentiment states to abstract game-theoretic environments:

wait_and_watch

range_bound

defensive_risk

Also estimates information asymmetry:

low

medium

high

This represents how uncertain or incomplete the public signal environment is.

5.5 Strategy Recommendation

strategy_recommender.py

Converts game states into rational strategic postures, such as:

hold_and_monitor

tactical_hold

avoid_or_hedge

Each recommendation is accompanied by a human-readable rationale.

5.6 Visualization

html_dashboard_generator.py

Generates a static HTML dashboard using inline CSS

No frameworks or external dependencies

Designed for offline demos and reviews

6. What This PoC Is — and Is Not
✅ What this PoC demonstrates

End-to-end system thinking

Clear separation of concerns

Explainable decision logic

Integration of NLP with strategy reasoning

❌ What this PoC does not claim

Market prediction accuracy

Trading or investment advice

Production readiness

Exhaustive data coverage

This scope is intentional.

7. Project Status

Work in Progress — PoC v1

Planned future iterations may include:

Temporal sentiment dynamics

Repeated-game modeling

More resilient ingestion pipelines

Scenario stress testing

Probabilistic state transitions

Feedback loops

8. Disclaimer

This project is for educational and exploratory purposes only.
It does not constitute financial, investment, or trading advice.

9. Closing Note

This PoC represents an idea in formation.
The current implementation prioritizes structure and reasoning over scale and optimization, serving as a foundation for future robustness and resilience.
