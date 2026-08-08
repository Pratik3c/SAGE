import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeneratedPost(BaseModel):

    text: str = Field(
        description="The final social media post."
    )

    rationale: str = Field(
        description="Why this topic was selected and why it is relevant now."
    )


def generate_post(topic, agent, memory=None):

    memory = memory or []

    memory_text = ""

    for item in memory:

        if item["type"] == "published_post":

            memory_text += f"""
Previously published post:
{item["text"]}
---
"""

        elif item["type"] == "evaluated_topic":

            memory_text += f"""
Previously evaluated topic:
{item["title"]}
Decision: {item["decision"]}
---
"""

    prompt = f"""
You are {agent["name"]}, an autonomous AI and technology persona.

DOMAIN

{agent["domain"]}

IDENTITY

{agent["identity"]["description"]}

INTERESTS

{", ".join(agent["identity"]["interests"])}

TONE

{", ".join(agent["identity"]["tone"])}

EDITORIAL OPINIONS

{chr(10).join("- " + opinion for opinion in agent["identity"]["opinions"])}

TOPIC

Title:
{topic["title"]}

Source:
{topic["source"]}

URL:
{topic["url"]}

Summary:
{topic.get("summary", "")}

MEMORY

{memory_text}

TASK

Write one original technology-focused social media post
based on the topic.

The post must:

- sound like the established persona
- focus on the actual technological development
- avoid generic AI hype
- avoid clickbait
- avoid inventing facts
- avoid copying the source
- provide useful technical insight
- be concise and readable
- clearly communicate why the development matters

The post should feel like an informed technology analyst
wrote it, not like a news article summarizer.

Do not mention that you are an AI.

Do not use hashtags excessively.

RATIONALE

Explain:

1. Why this topic was selected.
2. Why it is relevant now.
3. Why it fits the persona.

Return only the structured response.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GeneratedPost,
        },
    )

    return GeneratedPost.model_validate_json(
        response.text
    )