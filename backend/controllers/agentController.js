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

            identity: {
                description:
                    "An autonomous AI technology analyst that monitors the technology ecosystem and publishes only developments that are technically meaningful, relevant, and worth discussing.",

                interests: [
                    "Artificial Intelligence",
                    "AI Agents",
                    "Machine Learning",
                    "AI Security",
                    "Developer Tools",
                    "Open Source AI",
                    "AI Infrastructure"
                ],

                tone: [
                    "analytical",
                    "technical",
                    "concise",
                    "skeptical",
                    "evidence-driven"
                ],

                opinions: [
                    "Prefer substance over AI hype.",
                    "Technical significance matters more than popularity.",
                    "Primary sources are more valuable than recycled commentary.",
                    "Not every AI announcement deserves attention."
                ]
            },

            publishingRules: {
                minimumScore: 0.70,
                maxPostsPerDay: 4,
                avoidDuplicates: true
            }
        });

        return res.status(201).json({
            agentId: agent.agentId
        });

    } catch (error) {
        console.error("Agent initialization error:", error);

        return res.status(500).json({
            error: "Failed to initialize agent"
        });
    }
};


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


const getAgent = async (req, res) => {
    try {
        const { agentId } = req.params;

        const agent = await Agent.findOne({
            agentId
        }).lean();

        if (!agent) {
            return res.status(404).json({
                error: "Agent not found"
            });
        }

        return res.status(200).json({
            agent
        });

    } catch (error) {
        console.error("Agent retrieval error:", error);

        return res.status(500).json({
            error: "Failed to retrieve agent"
        });
    }
};


module.exports = {
    initializeAgent,
    getFeed,
    getAgent
};