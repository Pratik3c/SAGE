from database import (
    get_agent,
    get_pending_topics,
    get_recent_posts,
    get_recent_topics,
    update_topic_decision
)

from memory import build_memory_context

from editorial import evaluate_topic

AGENT_ID = "e07dbcf8-2b48-4522-952c-ef190a0301fe"


def main():

    agent = get_agent(AGENT_ID)

    if not agent:
        print("Agent not found.")
        return

    topics = get_pending_topics(
        AGENT_ID,
        limit=5
    )

    posts = get_recent_posts(
        AGENT_ID,
        limit=10
    )

    previous_topics = get_recent_topics(
        AGENT_ID,
        limit=20
    )

    memory = build_memory_context(
        posts,
        previous_topics
    )

    print(
        f"Loaded {len(posts)} previous posts"
    )

    print(
        f"Loaded {len(previous_topics)} previous topics"
    )

    print(
        f"Evaluating {len(topics)} new topics\n"
    )

    for topic in topics:

        print("=" * 70)

        print(
            "TOPIC:",
            topic["title"]
        )

        try:

            decision = evaluate_topic(
                topic,
                agent,
                memory
            )

            update_topic_decision(
                topic["topicId"],
                decision.decision,
                decision.score,
                decision.reason
            )

            print(
                "\nDECISION:",
                decision.decision
            )

            print(
                "SCORE:",
                decision.score
            )

            print(
                "\nREASON:",
                decision.reason
            )

        except Exception as error:

            print(
                "Gemini error:",
                error
            )


if __name__ == "__main__":
    main()