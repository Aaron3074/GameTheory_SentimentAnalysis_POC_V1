import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

from config import COMPANIES, MIN_ARTICLE_LENGTH

# --------------------------------------------------
# Ensure data directory exists
# --------------------------------------------------
os.makedirs("data", exist_ok=True)

# --------------------------------------------------
# DNS-safe Indian business RSS feeds
# --------------------------------------------------
RSS_FEEDS = {
    "Economic Times": "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
    "LiveMint": "https://www.livemint.com/rss/news"
}

# --------------------------------------------------
# Fetch RSS feed
# --------------------------------------------------
def fetch_rss(feed_url, source):
    try:
        response = requests.get(
            feed_url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response.content, "xml")

        rows = []
        for item in soup.find_all("item"):
            rows.append({
                "headline": item.title.text if item.title else "",
                "link": item.link.text if item.link else "",
                "source": source
            })

        return pd.DataFrame(rows)

    except Exception:
        return pd.DataFrame()

# --------------------------------------------------
# Scrape article text
# --------------------------------------------------
def scrape_article_text(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        return text
    except Exception:
        return ""

# --------------------------------------------------
# Main ingestion pipeline
# --------------------------------------------------
def run_news_ingestion():

    # Step 1: Pull RSS items
    rss_frames = []
    for source, url in RSS_FEEDS.items():
        print(f"Fetching from {source}")
        df = fetch_rss(url, source)
        rss_frames.append(df)

    news_df = pd.concat(rss_frames, ignore_index=True)

    if news_df.empty:
        print("No RSS data fetched.")
        return pd.DataFrame()

    final_rows = []

    # Step 2: Scrape + classify
    for _, row in news_df.iterrows():
        content = scrape_article_text(row["link"])

        if len(content) < MIN_ARTICLE_LENGTH:
            continue

        for company, keywords in COMPANIES.items():
            if any(keyword.lower() in content.lower() for keyword in keywords):
                final_rows.append({
                    "headline": row["headline"],
                    "link": row["link"],
                    "source": row["source"],
                    "content": content,
                    "company": company,
                    "scraped_at": datetime.now()
                })

    if not final_rows:
        print("No valid articles collected for any company.")
        return pd.DataFrame()

    final_df = pd.DataFrame(final_rows)
    final_df = final_df.drop_duplicates(subset=["headline", "company"])

    final_df.to_csv("data/news_raw.csv", index=False)
    print(f"Saved: data/news_raw.csv ({len(final_df)} rows)")

    return final_df

# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    run_news_ingestion()
