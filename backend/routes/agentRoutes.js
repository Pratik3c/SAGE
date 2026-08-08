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