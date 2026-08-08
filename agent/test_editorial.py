from database import get_agent, get_pending_topics
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

    print(f"Found {len(topics)} pending topics\n")

    for topic in topics:

        print("=" * 70)

        print("TOPIC:")
        print(topic["title"])

        try:

            decision = evaluate_topic(
                topic,
                agent
            )

            print("\nDECISION:", decision.decision)
            print("SCORE:", decision.score)

            print("Relevance:", decision.relevance)
            print("Novelty:", decision.novelty)
            print("Importance:", decision.importance)
            print("Persona Fit:", decision.persona_fit)

            print("\nREASON:")
            print(decision.reason)

        except Exception as error:

            print("Gemini error:", error)


if __name__ == "__main__":
    main()