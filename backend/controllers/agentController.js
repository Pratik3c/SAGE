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
            domain: persona.domain
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
            createdAt: post.createdAt.toISOString(),
            text: post.text,
            rationale: post.rationale,
            sources: post.sources
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


module.exports = {
    initializeAgent,
    getFeed
};