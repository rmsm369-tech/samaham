import feedparser
import json
from datetime import datetime

RSS_FEEDS = [
    "http://export.arxiv.org/rss/cs.AI",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://techcrunch.com/feed/",
]

def fetch_rss_news(max_per_feed=3):
    all_news = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_per_feed]:
                all_news.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", "")[:200],
                    "link": entry.get("link", ""),
                    "time": datetime.now().isoformat()
                })
        except:
            continue
    return all_news

if __name__ == "__main__":
    news = fetch_rss_news()
    for n in news:
        print(n["title"])
    print(f"\nFetched {len(news)} articles ✓")