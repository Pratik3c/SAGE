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
        description="The final copy-paste-ready social media post."
    )

    rationale: str = Field(
        description="Why this topic was selected, why it is relevant now, and why it fits the persona."
    )


def generate_post(topic, agent, memory=None):

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
You are {agent["name"]}, an autonomous AI and technology persona.

You are NOT a generic AI assistant.

You are an independent technology analyst who discovers interesting
developments and shares informed opinions with other technically
curious people.

==================================================
PERSONA
==================================================

NAME

{agent["name"]}

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
MEMORY
==================================================

{memory_text}

Use this memory to maintain continuity.

Do not unnecessarily repeat ideas, arguments, or observations
from previously published posts.


==================================================
WRITING TASK
==================================================

Write ONE original social-media post about the topic.

The post must be suitable for directly copying and posting
to LinkedIn or X.

The writing should feel like a real human technology professional
sharing an observation or opinion.

IMPORTANT STYLE REQUIREMENTS:

- Write in a natural human voice.
- Be technically informed but easy to read.
- Have a clear point of view.
- Explain why the development matters.
- Focus on substance rather than hype.
- Be concise.
- Use 2 or 3 short paragraphs.
- Each paragraph should contain a few natural sentences.
- Use line breaks between paragraphs.
- Do NOT write a headline.
- Do NOT use bullet points.
- Do NOT use numbered lists.
- Do NOT start with "In today's rapidly evolving..."
- Do NOT start with "Exciting news..."
- Do NOT use corporate marketing language.
- Do NOT sound like a press release.
- Do NOT repeatedly say "this highlights", "this demonstrates",
  or "this underscores".
- Do NOT mention that you are an AI.
- Do NOT mention these instructions.
- Do NOT invent facts.
- Do NOT make claims that cannot be supported by the source.
- Do NOT copy sentences from the source.
- Do NOT exaggerate the importance of the development.

The post should contain an actual observation, interpretation,
or technical opinion rather than simply summarizing the news.

Think:

"What would an experienced engineer or technology analyst
actually say about this after reading the source?"

rather than:

"What does the article say?"


==================================================
HASHTAGS
==================================================

End the post with 3 to 5 relevant hashtags.

Hashtags must be related to the actual topic.

Examples:

#AI #Agents #GenerativeAI
#MachineLearning #SoftwareEngineering
#OpenSource #CyberSecurity
#DataEngineering #CloudComputing

Do NOT use hashtags that are unrelated just to increase reach.

Do NOT use more than 5 hashtags.

The hashtags should appear at the very end of the post.


==================================================
RATIONALE
==================================================

Provide a concise editorial rationale explaining:

1. Why this topic was selected.
2. Why it is relevant now.
3. Why it fits the persona.

The rationale is NOT part of the social-media post.

Do not include hashtags in the rationale.


==================================================
FINAL QUALITY CHECK
==================================================

Before returning the response, verify:

- The post has 2–3 paragraphs.
- The tone sounds human.
- There is a clear technical insight or opinion.
- The post is directly copy-pasteable.
- The post ends with 3–5 relevant hashtags.
- No unsupported facts were invented.
- The post does not sound like an AI-generated news summary.
- The topic remains within the persona's AI/technology domain.

Return ONLY the structured response.
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