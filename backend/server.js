import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import pkg from "pg";

dotenv.config();
const { Pool } = pkg;

const app = express();
app.use(cors());
app.use(express.json());

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.get("/api/hello", (req, res) => {
  res.json({ message: "Hello from Node.js backend!" });
});

app.get("/api/users", async (req, res) => {
  const result = await pool.query("SELECT NOW()");
  res.json({ db_time: result.rows[0] });
});

app.listen(4000, () => console.log("✅ Backend running on port 4000"));
