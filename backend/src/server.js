require("dotenv").config();

const express = require("express");
const cors = require("cors");

const connectDB = require("../config/db");
const agentRoutes = require("../routes/agentRoutes");

const app = express();


// --------------------------------------------------
// Middleware
// --------------------------------------------------

app.use(cors());
app.use(express.json());


// --------------------------------------------------
// Database
// --------------------------------------------------

connectDB();


// --------------------------------------------------
// Health / Root
// --------------------------------------------------

app.get("/", (req, res) => {
    res.json({
        name: "SAGE API",
        status: "online"
    });
});


app.get("/health", (req, res) => {
    res.status(200).json({
        status: "healthy",
        service: "SAGE API",
        timestamp: new Date().toISOString()
    });
});


// --------------------------------------------------
// Agent Routes
// --------------------------------------------------

app.use(
    "/api/agent",
    agentRoutes
);


// --------------------------------------------------
// Export Express App
// --------------------------------------------------

module.exports = app;


// --------------------------------------------------
// Local Development Server
// --------------------------------------------------
//
// Vercel will NOT execute this section.
// It only runs when you execute:
//
// npm run dev
// or
// npm start
//
// --------------------------------------------------

if (require.main === module) {

    const PORT = process.env.PORT || 5000;

    app.listen(
        PORT,
        "0.0.0.0",
        () => {
            console.log(
                `SAGE API running on port ${PORT}`
            );
        }
    );
}