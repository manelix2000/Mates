import express from "express";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA_DIR = path.join(__dirname, "data");
const DATA_FILE = path.join(DATA_DIR, "progress.json");
const DIST_DIR = path.join(ROOT, "dist");

const PORT = Number(process.env.PORT) || 3001;

const app = express();
app.use(express.json({ limit: "256kb" }));

let writeChain = Promise.resolve();
function withLock(fn) {
  const next = writeChain.then(fn, fn);
  writeChain = next.catch(() => {});
  return next;
}

async function ensureDataFile() {
  await fs.mkdir(DATA_DIR, { recursive: true });
  try {
    await fs.access(DATA_FILE);
  } catch {
    await fs.writeFile(DATA_FILE, JSON.stringify({ version: 1, topics: {} }, null, 2), "utf8");
  }
}

async function readData() {
  await ensureDataFile();
  const raw = await fs.readFile(DATA_FILE, "utf8");
  try {
    const parsed = JSON.parse(raw);
    if (parsed && parsed.version === 1 && parsed.topics && typeof parsed.topics === "object") {
      return parsed;
    }
  } catch {
    // fichero corrupto: estructura vacía por defecto
  }
  return { version: 1, topics: {} };
}

async function writeData(data) {
  const tmp = DATA_FILE + ".tmp";
  await fs.writeFile(tmp, JSON.stringify(data, null, 2), "utf8");
  await fs.rename(tmp, DATA_FILE);
}

const TOPIC_ID_RE = /^[a-z0-9][a-z0-9-]{0,63}$/i;
const QUESTION_ID_RE = /^[a-z0-9_-]{1,64}$/i;

const validTopicId = (id) => typeof id === "string" && TOPIC_ID_RE.test(id);
const validQuestionId = (id) => typeof id === "string" && QUESTION_ID_RE.test(id);

app.get("/api/progress", async (_req, res) => {
  try {
    res.json(await readData());
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "read_failed" });
  }
});

app.get("/api/progress/:topicId", async (req, res) => {
  const { topicId } = req.params;
  if (!validTopicId(topicId)) return res.status(400).json({ error: "invalid_topic" });
  try {
    const data = await readData();
    res.json(data.topics[topicId] ?? { version: 1, answered: {} });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "read_failed" });
  }
});

app.post("/api/progress/:topicId/answer", async (req, res) => {
  const { topicId } = req.params;
  const { questionId, correct } = req.body ?? {};
  if (!validTopicId(topicId)) return res.status(400).json({ error: "invalid_topic" });
  if (!validQuestionId(questionId)) return res.status(400).json({ error: "invalid_question" });
  if (typeof correct !== "boolean") return res.status(400).json({ error: "invalid_correct" });

  try {
    const topic = await withLock(async () => {
      const data = await readData();
      const t = data.topics[topicId] ?? { version: 1, answered: {} };
      t.answered[questionId] = { correct, at: new Date().toISOString() };
      data.topics[topicId] = t;
      await writeData(data);
      return t;
    });
    res.json(topic);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "write_failed" });
  }
});

app.delete("/api/progress/:topicId", async (req, res) => {
  const { topicId } = req.params;
  if (!validTopicId(topicId)) return res.status(400).json({ error: "invalid_topic" });
  try {
    await withLock(async () => {
      const data = await readData();
      delete data.topics[topicId];
      await writeData(data);
    });
    res.json({ ok: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "write_failed" });
  }
});

try {
  await fs.access(DIST_DIR);
  app.use(express.static(DIST_DIR));
  app.get("*", (req, res, next) => {
    if (req.path.startsWith("/api/")) return next();
    res.sendFile(path.join(DIST_DIR, "index.html"));
  });
} catch {
  // sin build aún: el servidor sólo expone /api; en dev Vite sirve el SPA con proxy.
}

app.listen(PORT, () => {
  console.log(`[mates1] API en http://localhost:${PORT}`);
});
