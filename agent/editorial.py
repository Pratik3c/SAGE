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
technology persona.

MEMORY

SAGE has previously encountered the following information:

{memory_text}

Use this memory to avoid repetitive publishing.

A topic should be rejected if it substantially repeats something
SAGE has already published.

A topic can still be published if it is a genuinely new development
or provides a materially different angle.

MEMORY RULE

You must distinguish between:

1. Exact repetition
2. Substantial repetition
3. Related but genuinely new information

Exact repetition:
REJECT.

Substantial repetition without meaningful new information:
REJECT.

Related topic with significant new evidence, development,
benchmark, release, security event, research result, or
technical insight:
It may still be PUBLISHED.

Do not reject a topic merely because it belongs to the
same general area as an older topic.

PERSONA

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

TOPIC

Title:
{topic["title"]}

Source:
{topic["source"]}

URL:
{topic["url"]}

Summary:
{topic.get("summary", "")}

TASK

Decide whether this topic deserves publication.

The persona should NOT publish something merely because it
is popular or related to AI.

Prefer topics that:

- have genuine technical significance
- are relevant to AI and technology
- provide meaningful information
- have credible sourcing
- fit the persona's interests
- contain something worth discussing
- are sufficiently novel

Reject topics that are:

- generic
- repetitive
- promotional
- low-information
- unrelated to the persona
- clickbait
- trivial
- merely popular without substance

Return a score from 0 to 1.

The decision MUST be:

PUBLISH if the score meets or exceeds the publishing threshold.

REJECT otherwise.

Explain the decision clearly.
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