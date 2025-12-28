import pandas as pd
import re

from config import COMPANIES

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv("data/news_raw.csv")

# Lowercase content for matching
df["content_lower"] = df["content"].str.lower()

# Build keyword map
company_keywords = {
    company: [k.lower() for k in keywords]
    for company, keywords in COMPANIES.items()
}

# Macro keywords (very small, on purpose)
MACRO_KEYWORDS = [
    "inflation", "interest rate", "rbi", "fed",
    "policy", "budget", "ipo", "sensex",
    "nifty", "market", "economy", "gdp"
]

# --------------------------------------------------
# Helper: count company mentions
# --------------------------------------------------
def count_company_mentions(text):
    count = 0
    for keywords in company_keywords.values():
        for kw in keywords:
            if re.search(rf"\b{kw}\b", text):
                count += 1
                break
    return count

# --------------------------------------------------
# Helper: detect macro context
# --------------------------------------------------
def has_macro_signal(text):
    return any(kw in text for kw in MACRO_KEYWORDS)

# --------------------------------------------------
# Article type classification
# --------------------------------------------------
def classify_article(row):
    text = row["content_lower"]

    company_mentions = count_company_mentions(text)
    macro_flag = has_macro_signal(text)

    if company_mentions <= 1 and not macro_flag:
        return "company_specific"
    elif company_mentions <= 3:
        return "sector_market"
    else:
        return "macro"

# --------------------------------------------------
# Apply classification
# --------------------------------------------------
df["article_type"] = df.apply(classify_article, axis=1)

# Cleanup
df.drop(columns=["content_lower"], inplace=True)

# Save updated file
df.to_csv("data/news_day1_final.csv", index=False)

print("Saved: data/news_day1_final.csv")
print(df["article_type"].value_counts())
