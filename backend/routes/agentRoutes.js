const express = require("express");

const {
    initializeAgent,
    getFeed
} = require("../controllers/agentController");

const router = express.Router();

router.post("/init", initializeAgent);

router.get("/feed", getFeed);

module.exports = router;