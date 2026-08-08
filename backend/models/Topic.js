const mongoose = require("mongoose");

const topicSchema = new mongoose.Schema(
    {
        topicId: {
            type: String,
            required: true,
            unique: true
        },

        agentId: {
            type: String,
            required: true,
            index: true
        },

        title: {
            type: String,
            required: true
        },

        url: {
            type: String,
            required: true
        },

        source: {
            type: String,
            required: true
        },

        summary: {
            type: String
        },

        decision: {
            type: String,
            enum: ["PENDING", "PUBLISH", "REJECT"],
            default: "PENDING"
        },

        score: {
            type: Number,
            default: 0
        },

        reason: {
            type: String
        },

        discoveredAt: {
            type: Date,
            default: Date.now
        }
    }
);

module.exports = mongoose.model("Topic", topicSchema);