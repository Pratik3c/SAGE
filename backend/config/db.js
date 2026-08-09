const dns = require("dns");

dns.setServers([
  "8.8.8.8",
  "8.8.4.4"
]);

// const mongoose = require("mongoose");

// const connectDB = async () => {
//     try {
//         await mongoose.connect(process.env.MONGODB_URI);

//         console.log("MongoDB connected");
//     } catch (error) {
//         console.error("MongoDB connection failed:", error.message);
//         process.exit(1);
//     }
// };

// module.exports = connectDB;


const mongoose = require("mongoose");

let cachedConnection = null;
let cachedPromise = null;

const connectDB = async () => {
    // Already connected
    if (cachedConnection) {
        return cachedConnection;
    }

    // Connection is already being established
    if (cachedPromise) {
        cachedConnection = await cachedPromise;
        return cachedConnection;
    }

    if (!process.env.MONGODB_URI) {
        throw new Error(
            "MONGODB_URI environment variable is not defined"
        );
    }

    cachedPromise = mongoose.connect(
        process.env.MONGODB_URI
    );

    try {
        cachedConnection = await cachedPromise;

        console.log("MongoDB connected");

        return cachedConnection;

    } catch (error) {

        // Reset promise so a future invocation
        // can try connecting again.
        cachedPromise = null;

        console.error(
            "MongoDB connection failed:",
            error.message
        );

        throw error;
    }
};

module.exports = connectDB;