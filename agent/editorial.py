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


def evaluate_topic(topic, agent):

    prompt = f"""
You are the editorial decision engine for an autonomous AI
technology persona.

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
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": EditorialDecision,
        },
    )

    return EditorialDecision.model_validate_json(
        response.text
    )