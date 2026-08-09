import uuid
from datetime import datetime, timezone

from database import (
    create_post,
    update_agent_last_published
)

from writer import generate_post


def publish_topic(topic, agent, memory):

    generated = generate_post(
        topic,
        agent,
        memory
    )

    post_id = str(uuid.uuid4())

    created_at = datetime.now(
        timezone.utc
    )

    create_post(
        post_id=post_id,
        agent_id=agent["agentId"],
        text=generated.text,
        rationale=generated.rationale,
        sources=[topic["url"]],
        created_at=created_at
    )

    update_agent_last_published(
        agent["agentId"]
    )

    return {
        "postId": post_id,
        "createdAt": created_at.isoformat(),
        "text": generated.text,
        "rationale": generated.rationale,
        "sources": [topic["url"]]
    }