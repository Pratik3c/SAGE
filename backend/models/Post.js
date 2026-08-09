const mongoose = require("mongoose");

const postSchema = new mongoose.Schema(
    {
        postId: {
            type: String,
            required: true,
            unique: true
        },

        agentId: {
            type: String,
            required: true,
            index: true
        },

        text: {
            type: String,
            required: true
        },

        rationale: {
            type: String,
            required: true
        },

        sources: {
            type: [String],
            default: []
        },

        createdAt: {
            type: Date,
            default: Date.now,
            index: true
        }
    }
);

module.exports = mongoose.model("Post", postSchema);