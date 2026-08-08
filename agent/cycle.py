from datetime import datetime, timezone

from discovery import discover_topics

from database import (
    get_agent,
    get_pending_topics,
    get_recent_posts,
    get_recent_topics,
    save_topics,
    update_topic_decision,
    update_agent_last_run
)

from memory import build_memory_context
from editorial import evaluate_topic
from publisher import publish_topic


def run_cycle(agent_id):

    run_started_at = datetime.now(timezone.utc)

    print("=" * 60)
    print("VANTA AUTONOMOUS CYCLE")
    print("=" * 60)

    print(
        f"Run started: {run_started_at.isoformat()}"
    )

    try:

        # --------------------------------------------------
        # 1. Load Agent
        # --------------------------------------------------

        agent = get_agent(agent_id)

        if not agent:
            print("Agent not found.")
            return

        print(
            f"Agent: {agent['name']}"
        )

        # --------------------------------------------------
        # 2. Discover New Topics
        # --------------------------------------------------

        print("\nDiscovering new topics...")

        discovered_topics = discover_topics()

        print(
            f"Discovered {len(discovered_topics)} topics."
        )

        # --------------------------------------------------
        # 3. Save New Topics
        # --------------------------------------------------

        saved_topics = save_topics(
            discovered_topics,
            agent_id
        )

        print(
            f"Saved {saved_topics} new topics."
        )

        # --------------------------------------------------
        # 4. Get Pending Topics
        # --------------------------------------------------

        topics = get_pending_topics(
            agent_id,
            limit=5
        )

        print(
            f"Pending topics to evaluate: {len(topics)}"
        )

        if not topics:

            print("No pending topics.")

            update_agent_last_run(
                agent_id
            )

            return

        # --------------------------------------------------
        # 5. Load Memory
        # --------------------------------------------------

        posts = get_recent_posts(
            agent_id,
            limit=10
        )

        previous_topics = get_recent_topics(
            agent_id,
            limit=20
        )

        memory = build_memory_context(
            posts,
            previous_topics
        )

        print(
            f"Loaded {len(posts)} previous posts."
        )

        print(
            f"Loaded {len(previous_topics)} previous topics."
        )

        # --------------------------------------------------
        # 6. Editorial Evaluation
        # --------------------------------------------------

        published_count = 0

        max_posts_per_day = agent[
            "publishingRules"
        ]["maxPostsPerDay"]

        for topic in topics:

            print("\n" + "-" * 60)

            print(
                "TOPIC:",
                topic["title"]
            )

            try:

                # ------------------------------------------
                # Editorial Judgment
                # ------------------------------------------

                decision = evaluate_topic(
                    topic,
                    agent,
                    memory
                )

                print(
                    f"Decision: {decision.decision}"
                )

                print(
                    f"Score: {decision.score}"
                )

                print(
                    f"Reason: {decision.reason}"
                )

                # ------------------------------------------
                # Persist Editorial Decision
                # ------------------------------------------

                update_topic_decision(
                    topic["topicId"],
                    decision.decision,
                    decision.score,
                    decision.reason
                )

                # ------------------------------------------
                # Reject
                # ------------------------------------------

                if decision.decision != "PUBLISH":

                    print(
                        "Topic rejected."
                    )

                    continue

                # ------------------------------------------
                # Publishing Limit
                # ------------------------------------------

                if published_count >= max_posts_per_day:

                    print(
                        "Publishing limit reached."
                    )

                    break

                # ------------------------------------------
                # Generate + Publish
                # ------------------------------------------

                print(
                    "Generating post..."
                )

                post = publish_topic(
                    topic,
                    agent,
                    memory
                )

                print(
                    "\nPUBLISHED:"
                )

                print(
                    post["text"]
                )

                print(
                    "\nRATIONALE:"
                )

                print(
                    post["rationale"]
                )

                print(
                    "\nSOURCE:"
                )

                print(
                    post["sources"]
                )

                published_count += 1

                # ------------------------------------------
                # Update In-Memory Context
                #
                # This prevents another topic in the same
                # cycle from generating repetitive content.
                # ------------------------------------------

                memory.append({
                    "type": "published_post",
                    "text": post["text"],
                    "createdAt": datetime.now(
                        timezone.utc
                    ).isoformat()
                })

            except Exception as error:

                print(
                    f"Failed processing topic: {error}"
                )

                # Continue processing the remaining topics.
                continue

        # --------------------------------------------------
        # 7. Update Agent Last Run
        # --------------------------------------------------

        update_agent_last_run(
            agent_id
        )

        # --------------------------------------------------
        # 8. Cycle Summary
        # --------------------------------------------------

        print("\n" + "=" * 60)

        print(
            f"Cycle completed successfully."
        )

        print(
            f"Topics discovered: {len(discovered_topics)}"
        )

        print(
            f"New topics saved: {saved_topics}"
        )

        print(
            f"Topics evaluated: {len(topics)}"
        )

        print(
            f"Posts published: {published_count}"
        )

        print(
            f"Run finished: "
            f"{datetime.now(timezone.utc).isoformat()}"
        )

        print("=" * 60)

    except Exception as error:

        print(
            "\nCRITICAL CYCLE ERROR:"
        )

        print(
            error
        )

        # We intentionally don't crash the process with
        # unhandled exceptions. GitHub Actions can complete
        # this run while the next scheduled run gets another
        # opportunity to operate.