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