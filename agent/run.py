from discovery import discover_topics
from database import topics_collection
import hashlib

def generate_topic_id(agent_id, url):

    digest = hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()[:16]

    return f"{agent_id}_{digest}"

def save_topics(topics, agent_id):

    saved = 0

    for topic in topics:

        existing = topics_collection.find_one({
            "agentId": agent_id,
            "url": topic["url"]
        })

        if existing:
            continue

        topic_document = {
            "topicId": generate_topic_id(agent_id, topic["url"]),
            "agentId": agent_id,
            "title": topic["title"],
            "url": topic["url"],
            "source": topic["source"],
            "summary": topic["summary"],
            "decision": "PENDING",
            "score": 0,
            "reason": "",
            "discoveredAt": topic["publishedAt"]
        }

        topics_collection.insert_one(topic_document)

        saved += 1

    return saved


def main():

    # Temporary development value.
    # We'll load active agents automatically later.
    agent_id = "e07dbcf8-2b48-4522-952c-ef190a0301fe"

    topics = discover_topics()

    print(f"Discovered {len(topics)} topics")

    saved = save_topics(topics, agent_id)

    print(f"Saved {saved} new topics")


if __name__ == "__main__":
    main()