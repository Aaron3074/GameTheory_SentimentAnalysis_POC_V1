import pandas as pd

# ---------------------------------------
# Config
# ---------------------------------------
INPUT_FILE = "data/news_day3_strategy.csv"
OUTPUT_FILE = "dashboard.html"

# ---------------------------------------
# Load data
# ---------------------------------------
df = pd.read_csv(INPUT_FILE)

# ---------------------------------------
# Styling helpers
# ---------------------------------------
def asymmetry_color(level):
    if level == "low":
        return "#2ecc71"   # green
    elif level == "medium":
        return "#f39c12"   # amber
    else:
        return "#e74c3c"   # red

def game_state_label(state):
    return state.replace("_", " ").title()

def strategy_label(strategy):
    return strategy.replace("_", " ").title()

# ---------------------------------------
# Build HTML rows
# ---------------------------------------
rows_html = ""

for _, row in df.iterrows():
    rows_html += f"""
    <tr>
        <td>{row['company']}</td>
        <td>{game_state_label(row['game_state'])}</td>
        <td style="color:{asymmetry_color(row['information_asymmetry'])}; font-weight:bold;">
            {row['information_asymmetry'].title()}
        </td>
        <td><b>{strategy_label(row['recommended_strategy'])}</b></td>
        <td style="max-width:400px;">{row['rationale']}</td>
    </tr>
    """

# ---------------------------------------
# Full HTML document
# ---------------------------------------
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Game Theory Sentiment Dashboard</title>
    <meta charset="UTF-8">

    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            padding: 40px;
        }}

        h1 {{
            text-align: center;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin-top: 30px;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background-color: #2c3e50;
            color: white;
        }}

        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}

        .legend {{
            margin-top: 30px;
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
        }}

        .legend span {{
            font-weight: bold;
        }}
    </style>
</head>

<body>

<h1>Game Theory + Sentiment Decision Dashboard</h1>

<p style="text-align:center; color:#555;">
This dashboard summarizes company-level strategic posture derived from financial news sentiment using game-theoretic reasoning.
</p>

<table>
    <tr>
        <th>Company</th>
        <th>Game State</th>
        <th>Information Asymmetry</th>
        <th>Recommended Strategy</th>
        <th>Rationale</th>
    </tr>
    {rows_html}
</table>

<div class="legend">
    <h3>Information Asymmetry Guide</h3>
    <p><span style="color:#2ecc71;">Low</span> — Stable narrative, high confidence</p>
    <p><span style="color:#f39c12;">Medium</span> — Mixed signals, partial clarity</p>
    <p><span style="color:#e74c3c;">High</span> — Uncertain or negative information environment</p>
</div>

</body>
</html>
"""

# ---------------------------------------
# Save file
# ---------------------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard generated → {OUTPUT_FILE}")
