import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser


# ============================================================
# RSS SOURCES
# ============================================================

RSS_FEEDS = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss",
        "limit": 10,
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "limit": 10,
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "limit": 10,
    },
    {
        "name": "OpenAI News",
        "url": "https://openai.com/news/rss.xml",
        "limit": 10,
    },
    {
        "name": "NVIDIA Developer Blog",
        "url": "https://developer.nvidia.com/blog/feed/",
        "limit": 10,
    },
    {
        "name": "NVIDIA AI Blog",
        "url": "https://blogs.nvidia.com/feed/",
        "limit": 10,
    },
    {
        "name": "AWS Machine Learning Blog",
        "url": "https://aws.amazon.com/blogs/machine-learning/feed/",
        "limit": 10,
    },
    {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed/",
        "limit": 10,
    },
    {
        "name": "Cloudflare Blog",
        "url": "https://blog.cloudflare.com/rss/",
        "limit": 10,
    },
]


# ============================================================
# CONFIGURATION
# ============================================================

MAX_TOPIC_AGE_DAYS = 7

# Used to prevent obviously empty/noisy entries.
MIN_TITLE_LENGTH = 8

# Words that frequently indicate useful technical content.
TECH_KEYWORDS = {
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "llm",
    "large language model",
    "generative ai",
    "agent",
    "agents",
    "robotics",
    "computer vision",
    "nlp",
    "model",
    "models",
    "inference",
    "training",
    "gpu",
    "cuda",
    "open source",
    "github",
    "developer",
    "software",
    "api",
    "database",
    "cloud",
    "security",
    "cybersecurity",
    "data",
    "mlops",
    "framework",
    "benchmark",
    "transformer",
    "neural",
}


# ============================================================
# HELPERS
# ============================================================

def normalize_text(text):
    """
    Remove HTML and normalize whitespace.
    """

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_published_date(entry):
    """
    Extract publication date from an RSS entry.

    feedparser usually provides *_parsed fields, but some
    feeds only provide strings.
    """

    # --------------------------------------------------------
    # feedparser parsed timestamp
    # --------------------------------------------------------

    for field in (
        "published_parsed",
        "updated_parsed",
        "created_parsed",
    ):

        parsed = entry.get(field)

        if parsed:

            try:

                return datetime(
                    *parsed[:6],
                    tzinfo=timezone.utc
                )

            except (TypeError, ValueError):
                pass

    # --------------------------------------------------------
    # String timestamps
    # --------------------------------------------------------

    for field in (
        "published",
        "updated",
        "created",
    ):

        value = entry.get(field)

        if not value:
            continue

        try:

            parsed = parsedate_to_datetime(value)

            if parsed.tzinfo is None:
                parsed = parsed.replace(
                    tzinfo=timezone.utc
                )

            return parsed.astimezone(
                timezone.utc
            )

        except (TypeError, ValueError, OverflowError):
            continue

    return None


def is_recent(published_at):
    """
    Return True if the topic is recent enough.

    Entries without a publication date are allowed because
    some RSS feeds do not expose one reliably.
    """

    if not published_at:
        return True

    age = datetime.now(
        timezone.utc
    ) - published_at

    return age.days <= MAX_TOPIC_AGE_DAYS


def is_technology_relevant(title, summary):
    """
    Lightweight local relevance filter.

    This prevents obviously irrelevant topics from reaching
    the Gemini editorial engine.
    """

    text = f"{title} {summary}".lower()

    for keyword in TECH_KEYWORDS:

        if keyword in text:
            return True

    return False


def normalize_url(url):
    """
    Normalize URLs so duplicate articles from feeds can be
    detected more reliably.
    """

    if not url:
        return ""

    url = url.strip()

    # Remove trailing slash.
    url = url.rstrip("/")

    # Remove common tracking parameters.
    url = re.sub(
        r"[?&](utm_source|utm_medium|utm_campaign|utm_term|utm_content)=[^&]+",
        "",
        url,
        flags=re.IGNORECASE
    )

    return url


# ============================================================
# DISCOVERY
# ============================================================

def discover_topics():

    topics = []

    seen_urls = set()

    print(
        f"Discovering topics from {len(RSS_FEEDS)} RSS sources..."
    )

    for feed_config in RSS_FEEDS:

        feed_name = feed_config["name"]
        feed_url = feed_config["url"]
        feed_limit = feed_config.get("limit", 10)

        print(
            f"  → Fetching {feed_name}"
        )

        try:

            feed = feedparser.parse(
                feed_url
            )

            # ------------------------------------------------
            # Feed-level validation
            # ------------------------------------------------

            if getattr(feed, "bozo", False):

                print(
                    f"    Warning: malformed RSS feed: {feed_name}"
                )

            entries = getattr(
                feed,
                "entries",
                []
            )

            if not entries:

                print(
                    f"    No entries found."
                )

                continue

            source_count = 0

            # ------------------------------------------------
            # Process entries
            # ------------------------------------------------

            for entry in entries[:feed_limit]:

                title = normalize_text(
                    entry.get(
                        "title",
                        ""
                    )
                )

                url = normalize_url(
                    entry.get(
                        "link",
                        ""
                    )
                )

                if not title or not url:
                    continue

                if len(title) < MIN_TITLE_LENGTH:
                    continue

                # --------------------------------------------
                # Duplicate URL
                # --------------------------------------------

                if url in seen_urls:
                    continue

                # --------------------------------------------
                # Summary
                # --------------------------------------------

                summary = normalize_text(
                    entry.get(
                        "summary",
                        ""
                    )
                )

                # Some feeds use description instead.
                if not summary:

                    summary = normalize_text(
                        entry.get(
                            "description",
                            ""
                        )
                    )

                # --------------------------------------------
                # Publication date
                # --------------------------------------------

                published_at = parse_published_date(
                    entry
                )

                # --------------------------------------------
                # Recency
                # --------------------------------------------

                if not is_recent(
                    published_at
                ):
                    continue

                # --------------------------------------------
                # Local technology relevance filter
                # --------------------------------------------

                if not is_technology_relevant(
                    title,
                    summary
                ):
                    continue

                # --------------------------------------------
                # Store topic
                # --------------------------------------------

                topic = {
                    "title": title,

                    "url": url,

                    "source": feed_name,

                    "summary": summary,

                    "publishedAt": published_at,
                }

                topics.append(
                    topic
                )

                seen_urls.add(
                    url
                )

                source_count += 1

            print(
                f"    Added {source_count} topics."
            )

        except Exception as error:

            print(
                f"    Failed to fetch "
                f"{feed_name}: {error}"
            )

    # ========================================================
    # FINAL SORT
    # ========================================================

    topics.sort(
        key=lambda topic: (
            topic["publishedAt"] is not None,
            topic["publishedAt"] or datetime.min.replace(
                tzinfo=timezone.utc
            )
        ),
        reverse=True
    )

    print(
        f"Discovery complete. "
        f"{len(topics)} relevant topics discovered."
    )

    return topics