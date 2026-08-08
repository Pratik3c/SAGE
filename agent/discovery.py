import feedparser
from datetime import datetime, timezone


RSS_FEEDS = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss"
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml"
    }
]


def discover_topics():

    topics = []

    for feed_config in RSS_FEEDS:

        try:
            feed = feedparser.parse(feed_config["url"])

            for entry in feed.entries[:15]:

                title = entry.get("title", "").strip()
                url = entry.get("link", "").strip()

                if not title or not url:
                    continue

                summary = entry.get("summary", "").strip()

                published_at = None

                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_at = datetime(
                        *entry.published_parsed[:6],
                        tzinfo=timezone.utc
                    )

                topics.append({
                    "title": title,
                    "url": url,
                    "source": feed_config["name"],
                    "summary": summary,
                    "publishedAt": published_at
                })

        except Exception as error:
            print(
                f"Failed to fetch {feed_config['name']}: {error}"
            )

    return topics