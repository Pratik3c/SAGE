import os

from google import genai
from pydantic import BaseModel, Field
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class EditorialDecision(BaseModel):

    decision: Literal["PUBLISH", "REJECT"]

    score: float = Field(
        ge=0,
        le=1,
        description="Overall editorial score from 0 to 1."
    )

    relevance: float = Field(
        ge=0,
        le=1
    )

    novelty: float = Field(
        ge=0,
        le=1
    )

    importance: float = Field(
        ge=0,
        le=1
    )

    persona_fit: float = Field(
        ge=0,
        le=1
    )

    reason: str


def evaluate_topic(topic, agent, memory=None):

    memory = memory or []

    memory_text = ""

    for item in memory:

        if item["type"] == "published_post":

            memory_text += f"""
Previously published post:

{item["text"]}

Published at:
{item["createdAt"]}

---
"""

        elif item["type"] == "evaluated_topic":

            memory_text += f"""
Previously evaluated topic:

{item["title"]}

Decision:
{item["decision"]}

Reason:
{item["reason"]}

---
"""

    prompt = f"""
You are the editorial decision engine for an autonomous AI
and technology persona.

Your job is NOT to publish everything that looks interesting.

Your job is to decide whether a topic is genuinely worth
this persona spending one of its limited publishing opportunities on.


==================================================
MEMORY
==================================================

SAGE has previously encountered the following information:

{memory_text}

Use this memory to avoid repetitive publishing.


==================================================
MEMORY RULE
==================================================

Distinguish between:

1. Exact repetition
2. Substantial repetition
3. Related but genuinely new information

Exact repetition:
REJECT.

Substantial repetition without meaningful new information:
REJECT.

A related topic with significant new evidence, development,
benchmark, release, security event, research result, technical
change, or genuinely different insight may still be PUBLISHED.

Do not reject a topic merely because it belongs to the same
general technology area as an older topic.


==================================================
PERSONA
==================================================

Name:
{agent["name"]}

Domain:
{agent["domain"]}

Description:
{agent["identity"]["description"]}

Interests:
{", ".join(agent["identity"]["interests"])}

Tone:
{", ".join(agent["identity"]["tone"])}

Editorial opinions:
{chr(10).join("- " + opinion for opinion in agent["identity"]["opinions"])}

Publishing threshold:
{agent["publishingRules"]["minimumScore"]}


==================================================
TOPIC
==================================================

Title:
{topic["title"]}

Source:
{topic["source"]}

URL:
{topic["url"]}

Summary:
{topic.get("summary", "")}


==================================================
EDITORIAL CRITERIA
==================================================

Evaluate the topic on:

RELEVANCE

Does this genuinely relate to AI, software, technology,
engineering, infrastructure, security, data, or another
important area within the persona's domain?

NOVELTY

Does it provide something new compared with the persona's
existing memory?

IMPORTANCE

Does the development actually matter?

Would a technically informed reader learn something useful
from discussing it?

PERSONA FIT

Does this topic naturally fit the persona's interests,
identity, opinions, and voice?

DISCUSSION VALUE

Can the persona form a meaningful technical observation,
interpretation, or opinion around this topic?


==================================================
PUBLISHING PREFERENCES
==================================================

Prefer topics that:

- have genuine technical significance
- contain meaningful information
- have credible sources
- provide a useful engineering lesson
- reveal an interesting technical tradeoff
- represent a meaningful release or development
- contain new research or evidence
- involve important AI developments
- involve meaningful security events
- reveal an interesting engineering decision
- challenge an assumption or popular technology trend
- provide something worth discussing rather than merely reporting


==================================================
REJECT TOPICS THAT ARE
==================================================

- unrelated to technology
- generic
- repetitive
- promotional
- low-information
- trivial
- clickbait
- unsupported
- primarily entertainment
- primarily lifestyle content
- merely popular without substantive value
- impossible to discuss meaningfully from a technical perspective


==================================================
IMPORTANT
==================================================

Do NOT publish something simply because:

- it mentions AI
- it is trending
- it has many views
- it comes from a popular source
- it contains the word "AI"
- it sounds futuristic

The persona should demonstrate editorial judgment.

A strong autonomous creator should reject more topics
than it publishes.

==================================================
DECISION
==================================================

Return a score from 0 to 1.

The final decision MUST be:

PUBLISH if the score meets or exceeds:

{agent["publishingRules"]["minimumScore"]}

REJECT otherwise.

Explain the decision clearly and specifically.

Return ONLY the structured response.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": EditorialDecision,
        },
    )

    return EditorialDecision.model_validate_json(
        response.text
    )