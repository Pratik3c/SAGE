# SAGE — Autonomous AI Creator
## Vibe Coding Conversation History

> This file documents the AI-assisted development process used to build SAGE.
> It intentionally preserves the iterative nature of the project: requirements,
> architecture decisions, implementation requests, debugging, deployment issues,
> and refinements.
>
> The transcript below is reconstructed from the actual project conversation
> available during development. It is kept conversational rather than rewritten
> as a polished specification.

---

# 1. Project Selection

### YOU

I want to build the Autonomous AI Creator hackathon project.

The agent should independently:
- Discover topics from live information sources
- Decide whether a topic is worth publishing
- Write in a consistent editorial voice
- Remember previously published content
- Continue publishing over time without additional human input

The evaluator will initialize the agent once and then periodically call the feed endpoint.

I want to build it free of cost as much as possible.

I know MERN, Python/Flask and MongoDB. Can we use GitHub Actions for autonomous execution?

Also, is Gemini usage mandatory, and will the free tier sustain it?

### CHATGPT

Yes. Gemini is not mandatory; the challenge allows any AI model.

A practical free architecture is:
- React for the frontend
- Node.js + Express for the API
- MongoDB Atlas free tier for persistence
- Python for the autonomous AI cycle
- Gemini API for editorial judgment and writing
- GitHub Actions for scheduled autonomous execution
- Vercel for the API/frontend deployment

The web server does not need to run the autonomous loop continuously. GitHub Actions can periodically wake up the Python agent, execute one autonomous cycle, store the results in MongoDB, and exit.

---

# 2. Choosing the Project

### YOU

There is another project option, The Interview Agent.

Which one is easier and more valuable?

### CHATGPT

The Interview Agent is technically more straightforward.

The Autonomous AI Creator is more unusual and potentially more valuable because fewer teams are likely to attempt true autonomous publishing over time.

For this hackathon, I would choose Autonomous AI Creator if the goal is differentiation.

### YOU

Let's go with Autonomous AI Creator.

Give me a name for this project only 10 options.

### CHATGPT

Possible names:
1. SAGE
2. VANTA
3. NEXUS
4. ORBIT
5. PULSE
6. Axiom
7. Signal
8. Vector
9. Forge
10. Sentinel

### YOU

I choose SAGE.

---

# 3. Prompt History Requirement

### YOU

They need prompts.md to see if it is vibe coded completely. Should I include chats in it?

### CHATGPT

Yes. For a vibe-coding hackathon, a conversation-style prompts.md is stronger than only listing final prompts.

It should show the iterative process:
- initial idea
- architecture
- implementation
- debugging
- changes
- deployment
- refinements

### YOU

Do I only need to include my prompts or the response of the LLM also?

### CHATGPT

Include both sides if the rules allow it.

The strongest format is:

YOU:
...

CHATGPT:
...

Then continue chronologically.

---

# 4. Architecture

### YOU

How can I make this project free of cost?

### CHATGPT

Use a mostly free architecture:

    RSS Sources
         ↓
    Python Discovery
         ↓
    MongoDB
         ↓
    Gemini Editorial Judgment
         ↓
    Publish?
       /   \
     NO    YES
            ↓
       Gemini Writer
            ↓
       MongoDB Posts
            ↓
       Express API
            ↓
        Evaluator

GitHub Actions periodically triggers the Python cycle.

---

# 5. Phase-Based Development
### YOU

Give the code phase wise,and i will let u know once the phase is completed.

### CHATGPT

<CODE give my CHATGPT\>

### YOU

Phase 0 done.

### CHATGPT

Great. Phase 0 is complete. Next we can establish the backend foundation and database models.
<CODE give my CHATGPT\>

### YOU

Phase 1 completed.

### CHATGPT

Good. Move to the next phase. The next stage is the autonomous agent/data layer: topic discovery, topic normalization, MongoDB persistence, editorial state, and memory.
<CODE give my CHATGPT\>

### YOU

Phase 2 completed.

### CHATGPT

Good. Continue with the editorial engine. Discovery and editorial judgment should remain separate. Discovery finds candidates; the editorial engine decides PUBLISH or REJECT with a score and explanation.
<CODE give my CHATGPT\>

### YOU

Phase 3 completed.

### CHATGPT

Great. Next connect writing and publishing:

Discovery → MongoDB → Editorial judgment → Writer → Publisher → MongoDB posts

<CODE give my CHATGPT\>

### YOU

Phase 4 completed.

### CHATGPT

Good. Now focus on memory and continuity. SAGE should remember previously published posts and previously evaluated topics.
<CODE give my CHATGPT\>

### YOU

Phase 5 completed.

### CHATGPT

Great. Next is autonomous execution. The cycle should load the agent, discover topics, save topics, load memory, evaluate, publish approved topics, update timestamps, and finish.
<CODE give my CHATGPT\>

### YOU

Phase 6 completed.

### CHATGPT

Good. Now move toward deployment and scheduled execution. The API handles evaluator requests; GitHub Actions handles periodic agent execution; MongoDB is the shared state.
<CODE give my CHATGPT\>

### YOU

Phase 7 completed.

### CHATGPT

Great. The core autonomous system is now in place. Next is deployment and making sure the evaluator can access the system without manual intervention.
<CODE give my CHATGPT\>

---

# 6. Vercel Deployment

### YOU

Can we deploy this on Vercel?

### CHATGPT

Yes. Vercel can host the Express API as a serverless function.

The important change is that the deployed serverless function should not depend on app.listen().

The Express application should be exported for Vercel while local development can still use app.listen().

GitHub Actions remains responsible for running the autonomous Python cycle.

### YOU

For now we have our project like this.

[Project structure screenshot shared]

### CHATGPT

The current structure is workable.

Keep the API-related files together and the Python autonomous agent separate.

A useful structure is:

    backend/
        src/
            server.js
            routes/
            controllers/
            models/

    agent/
        cycle.py
        discovery.py
        editorial.py
        writer.py
        publisher.py
        database.py

    .github/
        workflows/

---

# 7. Express / Vercel

### YOU

My server.js is which u gave me initially:

```javascript
require("dotenv").config();
const express = require("express");
const cors = require("cors");
const connectDB = require("../config/db");
const agentRoutes = require("../routes/agentRoutes");

const app = express();

connectDB();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
    res.json({
        name: "SAGE API",
        status: "online"
    });
});

app.use("/api/agent", agentRoutes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`SAGE API running on port ${PORT}`);
});
```

### CHATGPT

For Vercel, export the Express app so Vercel can invoke it as a serverless function. Keep local app.listen() behavior only where needed for local development.

---

# 8. Route Debugging

### YOU

Cannot GET /agent/feed

### CHATGPT

The deployed route and requested route do not match.

The intended public endpoint is:

    GET /api/agent/feed?agentId=...

Make sure Express mounts /api/agent, the router defines /feed, and Vercel forwards the request to Express.

### YOU

Yes it is working now, what should I do next? frontend?

### CHATGPT

The backend API and autonomous cycle should be verified end-to-end before the frontend. The frontend is optional for the evaluator because the required contract is HTTP/JSON.

---

# 9. Gemini Quota Issue

### YOU

Everything is working but API limit is getting exceeded.

The run shows:

```text
Discovered 45 topics.
Saved 6 new topics.
Pending topics to evaluate: 5

TOPIC: Don't use your phone while you poop
Decision: REJECT
Score: 0.05

TOPIC: Gentoo bugzilla closed due AI bot scraper overload
Failed processing topic: 429 RESOURCE_EXHAUSTED

TOPIC: Voyager 1 FDS Computer Emulator
Failed processing topic: 429 RESOURCE_EXHAUSTED
```

The Gemini error says the free-tier request quota was exceeded.

### CHATGPT

The first rejection demonstrates that editorial judgment is working, but too many Gemini requests are being made.

The architecture should minimize LLM calls:

RSS discovery
→ local relevance filtering
→ deduplication
→ only a small number of candidates
→ Gemini editorial judgment
→ Gemini writer only for approved topics

Do not use Gemini for deterministic discovery, URL deduplication, or obvious filtering.

---

# 10. Gemini Lite

### YOU

Gemini 3.1 Flash Lite -- Text-out models -- RPD is 500.

### CHATGPT

A higher request-per-day limit is much better for this architecture. Use the supported Lite model available to your API account and keep the API key unchanged.

### YOU

How can I use Gemini 3.5 Flash Lite? What changes do I need?

### CHATGPT

Change the model name in both the editorial and writer modules to:

```python
model="gemini-3.5-flash-lite"
```

Keep the same GEMINI_API_KEY.

### YOU

The API key will remain same?

### CHATGPT

Yes. The API key belongs to the Google AI project; the model is selected in the API request.

---

# 11. GitHub Actions Schedule

### YOU

Everything is working fine, I think we should change the time from 2 hrs to 8hr for now in github action and we will change the time back to 3-4 hrs before submitting project.

### CHATGPT

That is reasonable during development.

Use:

```yaml
on:
  schedule:
    - cron: "17 */8 * * *"

  workflow_dispatch:
```

Then change it to the desired final interval before submission.

### YOU

This is how it looks:

```yaml
name: SAGE Autonomous Agent

on:
  schedule:
    - cron: "17 */2 * * *"

  workflow_dispatch:

jobs:
```

### CHATGPT

Change the cron expression to:

```yaml
- cron: "17 */8 * * *"
```

Everything else can remain unchanged.

---

# 12. Feed Timestamp / Content Problem

### YOU

Before frontend, if we observe carefully, there is no createdAt field since we have to arrange the post as newest first.

Also it is just 1 para.

We want 2-3 paras with hashtags like #ai #agents #generativeAi at end so that it should be ready to copy & directly paste in LinkedIn or X.

It should look like post right? Natural human tone.

### CHATGPT

Yes.

The database must actually store createdAt at publication time.

The feed should sort by:

```javascript
.sort({
    createdAt: -1
})
```

The writer should produce 2–3 natural paragraphs and end with a small number of relevant hashtags.

Avoid:
- corporate language
- generic AI hype
- fake enthusiasm
- excessive formatting
- unsupported claims
- clickbait

---

# 13. Writer Code Review

### YOU

My writer is which u gave me initially:

```python
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
```

### CHATGPT

Keep the structured Pydantic response.

Strengthen the writer prompt so the post has:
- 2–3 paragraphs
- a natural human tone
- technical interpretation
- a useful takeaway
- 2–5 relevant hashtags
- no generic AI hype
- no unsupported claims
- no mention that it is AI-generated

---

# 14. Editorial Engine Review

### YOU

My editorial engine returns:

- decision
- score
- relevance
- novelty
- importance
- persona_fit
- reason

The publishing threshold is 0.70.

### CHATGPT

That is a strong structure.

Memory rules should distinguish:

Exact repetition → REJECT

Substantial repetition without meaningful new information → REJECT

Related topic with significant new evidence/development → MAY PUBLISH

New benchmark → MAY PUBLISH

New security event → MAY PUBLISH

New research result → MAY PUBLISH

New technical implementation → MAY PUBLISH

This makes the memory actually influence editorial decisions.

---

# 15. Publisher / createdAt Fix

### YOU

Here is publisher.py which u gave me initially if u don't remember:

```python
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

    create_post(
        post_id=post_id,
        agent_id=agent["agentId"],
        text=generated.text,
        rationale=generated.rationale,
        sources=[topic["url"]]
    )

    update_agent_last_published(
        agent["agentId"]
    )

    return {
        "postId": post_id,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "text": generated.text,
        "rationale": generated.rationale,
        "sources": [topic["url"]]
    }
```

### CHATGPT

The timestamp is returned by the publisher but not stored in MongoDB.

Pass the timestamp into create_post() and store it in the post document.

That ensures the API can reliably sort posts.

---

# 16. Database Review

### YOU

My database.py has if you have any further update, update it and give entire code back...

```python
def get_recent_posts(agent_id, limit=10):
    return list(
        posts_collection.find({
            "agentId": agent_id
        })
        .sort("createdAt", -1)
        .limit(limit)
    )
```

and:

```python
def create_post(
    post_id,
    agent_id,
    text,
    rationale,
    sources
):
    posts_collection.insert_one({
        "postId": post_id,
        "agentId": agent_id,
        "text": text,
        "rationale": rationale,
        "sources": sources
    })
```

### CHATGPT

get_recent_posts() is already sorting correctly.

The missing piece is create_post().

It needs to save:

```python
"createdAt": created_at
```

with a UTC timestamp.

---

# 17. Routes

### YOU

My agentRoutes.js is:

```javascript
const express = require("express");

const {
    initializeAgent,
    getFeed,
    getAgent
} = require("../controllers/agentController");

const router = express.Router();

router.post("/init", initializeAgent);
router.get("/feed", getFeed);
router.get("/:agentId", getAgent);

module.exports = router;
```

### CHATGPT

This is already correct.

With:

```javascript
app.use("/api/agent", agentRoutes);
```

the public routes are:

```text
POST /api/agent/init
GET /api/agent/feed
GET /api/agent/:agentId
```

No changes are required.

---

# 18. Controller Review

### YOU

My getFeed() is pls review it, if any updates to ur previous code:

```javascript
const getFeed = async (req, res) => {
    try {
        const { agentId } = req.query;

        if (!agentId) {
            return res.status(400).json({
                error: "agentId is required"
            });
        }

        const posts = await Post.find({
            agentId
        })
        .sort({
            createdAt: -1
        })
        .lean();

        const formattedPosts = posts.map((post) => ({
            id: post.postId,
            createdAt: post.createdAt
                ? new Date(post.createdAt).toISOString()
                : null,
            text: post.text,
            rationale: post.rationale,
            sources: post.sources || []
        }));

        return res.status(200).json({
            posts: formattedPosts
        });
    } catch (error) {
        console.error("Feed retrieval error:", error);

        return res.status(500).json({
            error: "Failed to retrieve feed"
        });
    }
};
```

### CHATGPT

This is already correct.

It:
- filters by agentId
- sorts newest first
- returns createdAt
- returns text
- returns rationale
- returns sources

---

# 19. Post Model

### YOU

models/Post.js contains createdAt.

### CHATGPT

Perfect.

Then the remaining requirement is to make sure the Python publisher/database actually writes createdAt into MongoDB.

Once new posts contain the field, the existing feed sorting will work.

---

# 20. Fixed DB error

### YOU

I am getting constant error from DB connection.

### CHATGPT

Add this in db.js, this will help to resolve the DNS error.

Use:

```text
const dns = require("dns");

dns.setServers([
"8.8.8.8",
"8.8.4.4"
]);
```

---

# 21. initializeAgent Update

### YOU

This was my initial code:

```javascript
const crypto = require("crypto");

const Agent = require("../models/Agent");
const Post = require("../models/Post");

const initializeAgent = async (req, res) => {
    try {
        const { persona } = req.body;

        if (!persona || !persona.name || !persona.domain) {
            return res.status(400).json({
                error: "persona.name and persona.domain are required"
            });
        }

        const agentId = crypto.randomUUID();

        const agent = await Agent.create({
            agentId,
            name: persona.name,
            domain: persona.domain,
            ...
        });

        return res.status(201).json({
            agentId: agent.agentId
        });
    } catch (error) {
        ...
    }
};
```

---

# 22. Mongoose Warning

### YOU

I got:

```text
(node:11388) [MONGOOSE] Warning:
mongoose: the `new` option for findOneAndUpdate()
and findOneAndReplace() is deprecated.
Use `returnDocument: 'after'` instead.
```

### CHATGPT

This is only a Mongoose 9 deprecation warning.

Replace:

```javascript
new: true
```

with:

```javascript
returnDocument: "after"
```

No behavior change is intended.

---

# 23. RSS Expansion

### YOU

Can we add more RSS feeds for more topics?

My current feeds are:

```python
RSS_FEEDS = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss"
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml"
    }
]
```

### CHATGPT

Yes. Add more high-quality sources across AI research, engineering, security, open source, infrastructure, developer tools, and cloud.

However, do not simply increase Gemini usage.

Use a pipeline:

```text
Many RSS feeds
      ↓
URL deduplication
      ↓
Recency filtering
      ↓
Local technical relevance filtering
      ↓
MongoDB duplicate check
      ↓
Gemini editorial judgment
```

---

# 24. Production Discovery

### YOU

Give me a clean production-ready discovery.py.

### CHATGPT

The production discovery layer should include:

- multiple RSS sources
- per-feed entry limits
- URL normalization
- tracking parameter removal
- duplicate detection
- publication date normalization
- stale-topic filtering
- lightweight technical relevance filtering
- graceful handling of malformed feeds
- logging
- continuing when one feed fails
- sorting by recency

It should not use Gemini.

That keeps discovery free and reduces API consumption.

---

# 25. Final Discovery Pipeline

### CHATGPT

The final discovery behavior is:

```text
15 RSS sources
       ↓
raw entries
       ↓
URL normalization
       ↓
duplicate removal
       ↓
date normalization
       ↓
recent content only
       ↓
technical relevance filter
       ↓
MongoDB duplicate check
       ↓
small pending pool
       ↓
Gemini editorial engine
```

The goal is to maximize topic diversity without sending every RSS entry to Gemini.

---

# 26. Autonomous Execution Model

### YOU

The server should continuously run, right?

The hackathon is 48 hours but evaluation is done afterwards for one week. We have to make the project live as well by deploying.

### CHATGPT

The HTTP API should stay deployed, but the autonomous loop does not need to be a permanently running server process.

Use:

```text
Vercel
→ Express API

MongoDB
→ persistent state

GitHub Actions
→ scheduled cycle

Python
→ discovery + editorial + publishing
```

GitHub Actions periodically wakes the agent, executes a cycle, writes to MongoDB, and exits.

The next scheduled run continues from the previous memory.

---

# 27. Frontend Decision

### YOU

Everything is working. Should we build a frontend?

### CHATGPT

Not necessary, first focus on the backend it should be stable.

The evaluator can use the JSON API without a frontend.

A frontend would improve the demo by showing:

- SAGE identity
- live feed
- timestamps
- rationale
- sources
- autonomous status
- last run
- last published time

It is presentation, not a requirement for the core evaluator.

---

# 28. Final Architecture

### CHATGPT

The final architecture is:

```text
                 RSS / LIVE SOURCES
                         |
                         v
                +------------------+
                | Python Discovery |
                +--------+---------+
                         |
                filtering + dedup
                         |
                         v
                +------------------+
                |     MongoDB      |
                | topics / memory  |
                | posts / agent    |
                +--------+---------+
                         |
                         v
                +------------------+
                | Gemini Editorial |
                |   PUBLISH/REJECT |
                +--------+---------+
                         |
                    PUBLISH?
                    /     \
                  NO       YES
                  |         |
                  |         v
                  |   +-------------+
                  |   | Gemini Writer|
                  |   +------+------+ 
                  |          |
                  +----------+
                             |
                             v
                       MongoDB Posts
                             |
                             +
                             |           
                             v                
                        Express API         
                             |
                             v
                          Evaluator

                      GitHub Actions
                            |
                            v
                    cycle.py periodically
```

---

# 29. Final Content Goal

### YOU

I want the post to look ready to copy and directly paste into LinkedIn or X.

### CHATGPT

The final writer should produce something like:

```text
Shopify moving inventory reservations from Redis to MySQL is an interesting reminder that scaling doesn't always mean adding another distributed system.

The important part isn't MySQL versus Redis. It's the workload. Inventory reservations need strong transactional guarantees, and a well-designed relational model can sometimes remove an entire layer of distributed coordination. That's a very different optimization strategy from simply reaching for the most scalable-looking technology.

The useful lesson: architecture should follow the consistency and workload requirements, not the popularity of the infrastructure stack.

#AI #Engineering #Databases
```

The API separately returns the rationale and original source.

---

# 30. Final Testing

### YOU

What should we test before submission?

### CHATGPT

Test the complete path:

```text
POST /api/agent/init
        ↓
fixed agent ID
        ↓
MongoDB agent
        ↓
GitHub Actions
        ↓
cycle.py
        ↓
RSS discovery
        ↓
deduplication
        ↓
editorial judgment
        ↓
writer
        ↓
MongoDB post
        ↓
GET /api/agent/feed
        ↓
newest-first feed
```

Verify:

- init works
- fixed agent ID is returned
- feed works
- createdAt is present
- posts are newest first
- sources are returned
- rationale is returned
- rejected topics remain in memory
- duplicate topics are avoided
- Gemini quota is respected
- GitHub Actions runs
- Vercel API remains live
- no secrets are committed
- no localhost dependency exists

---

# 31. Final SAGE Behavior

### CHATGPT

SAGE should not simply be:

```text
RSS → LLM → Post
```

It should behave more like:

```text
DISCOVER
   ↓
FILTER
   ↓
REMEMBER
   ↓
JUDGE
   ↓
WRITE
   ↓
PUBLISH
   ↓
REMEMBER
   ↓
WAIT
   ↓
DISCOVER AGAIN
```

The important part of the project is the editorial loop.

SAGE is autonomous because it decides what deserves attention rather than waiting for a human to provide a topic.

---

# 32. Final Project Identity

## SAGE

**Autonomous AI Technology Analyst**

SAGE monitors the technology ecosystem, evaluates what is actually worth discussing, remembers what it has already covered, and publishes only when a topic meets its editorial standards.

Core editorial principle:

> Not everything deserves to be published.

---

# 33. Final Development Philosophy

The project was built iteratively using AI-assisted/vibe coding.

The development process was:

```text
Idea
 ↓
Architecture
 ↓
Implementation
 ↓
Run
 ↓
Observe failure
 ↓
Ask AI for diagnosis
 ↓
Modify implementation
 ↓
Deploy
 ↓
Observe real behavior
 ↓
Refine prompts
 ↓
Optimize API usage
 ↓
Improve content quality
 ↓
Final submission
```

The AI assistant was used for:
- architecture decisions
- code generation
- debugging
- deployment guidance
- API design
- MongoDB design
- memory design
- prompt refinement
- quota optimization
- content quality
- autonomous execution design

---

# 34. Current Final State

SAGE has:

- live topic discovery
- multiple RSS sources
- local relevance filtering
- duplicate detection
- editorial judgment
- consistent persona
- persistent memory
- source attribution
- publishing rationale
- timestamped posts
- newest-first feed
- autonomous scheduled execution
- Gemini-powered writing
- MongoDB persistence
- Vercel API deployment
- GitHub Actions automation
- evaluator-compatible endpoints

The final autonomous loop is:

```text
DISCOVER → FILTER → REMEMBER → JUDGE → WRITE → PUBLISH → REMEMBER → WAIT
```

The evaluator only needs to initialize SAGE once and then retrieve the feed while the system continues operating autonomously.
