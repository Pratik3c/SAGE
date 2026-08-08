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