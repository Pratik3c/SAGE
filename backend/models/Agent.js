const mongoose = require("mongoose");

const agentSchema = new mongoose.Schema(
    {
        agentId: {
            type: String,
            required: true,
            unique: true,
            index: true
        },

        name: {
            type: String,
            required: true,
            trim: true
        },

        domain: {
            type: String,
            required: true,
            trim: true
        },

        identity: {
            description: {
                type: String,
                default: ""
            },

            interests: {
                type: [String],
                default: []
            },

            tone: {
                type: [String],
                default: []
            },

            opinions: {
                type: [String],
                default: []
            }
        },

        publishingRules: {
            minimumScore: {
                type: Number,
                default: 0.70
            },

            maxPostsPerDay: {
                type: Number,
                default: 4
            },

            avoidDuplicates: {
                type: Boolean,
                default: true
            }
        },

        active: {
            type: Boolean,
            default: true
        },

        lastRunAt: {
            type: Date,
            default: null
        },

        lastPublishedAt: {
            type: Date,
            default: null
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Agent", agentSchema);