import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["test"]

topics_collection = db["topics"]
agents_collection = db["agents"]
posts_collection = db["posts"]

def get_agent(agent_id):

    # print(agent_id)

    return agents_collection.find_one({
        "agentId": agent_id
    })

def get_pending_topics(agent_id, limit=5):

    return list(
        topics_collection.find({
            "agentId": agent_id,
            "decision": "PENDING"
        })
        .sort("discoveredAt", -1)
        .limit(limit)
    )

def get_recent_posts(agent_id, limit=10):

    return list(
        posts_collection.find({
            "agentId": agent_id
        })
        .sort("createdAt", -1)
        .limit(limit)
    )

def get_recent_topics(agent_id, limit=20):

    return list(
        topics_collection.find({
            "agentId": agent_id,
            "decision": {
                "$in": ["PUBLISH", "REJECT"]
            }
        })
        .sort("discoveredAt", -1)
        .limit(limit)
    )

def topic_url_exists(agent_id, url):

    return topics_collection.find_one({
        "agentId": agent_id,
        "url": url
    }) is not None

def update_topic_decision(
    topic_id,
    decision,
    score,
    reason
):

    topics_collection.update_one(
        {
            "topicId": topic_id
        },
        {
            "$set": {
                "decision": decision,
                "score": score,
                "reason": reason
            }
        }
    )


def create_post(
    post_id,
    agent_id,
    text,
    rationale,
    sources
):

    posts_collection.insert_one({
        "postId": post_id,
        "agentId": agent_id,
        "text": text,
        "rationale": rationale,
        "sources": sources
    })


def update_agent_last_published(agent_id):

    from datetime import datetime, timezone

    agents_collection.update_one(
        {
            "agentId": agent_id
        },
        {
            "$set": {
                "lastPublishedAt": datetime.now(timezone.utc)
            }
        }
    )

def generate_topic_id(agent_id, url):

    import hashlib

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
            "topicId": generate_topic_id(
                agent_id,
                topic["url"]
            ),

            "agentId": agent_id,

            "title": topic["title"],

            "url": topic["url"],

            "source": topic["source"],

            "summary": topic.get(
                "summary",
                ""
            ),

            "decision": "PENDING",

            "score": 0,

            "reason": "",

            "discoveredAt": topic.get(
                "publishedAt"
            )
        }

        topics_collection.insert_one(
            topic_document
        )

        saved += 1

    return saved



def update_agent_last_run(agent_id):

    from datetime import datetime, timezone

    agents_collection.update_one(
        {
            "agentId": agent_id
        },
        {
            "$set": {
                "lastRunAt": datetime.now(
                    timezone.utc
                )
            }
        }
    )