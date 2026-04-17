export type AnswerEntry = { correct: boolean; at: string };
export type TopicProgress = {
  version: 1;
  answered: Record<string, AnswerEntry>;
};

const cache = new Map<string, TopicProgress>();
const inflight = new Map<string, Promise<TopicProgress>>();

function empty(): TopicProgress {
  return { version: 1, answered: {} };
}

function isTopicProgress(value: unknown): value is TopicProgress {
  if (!value || typeof value !== "object") return false;
  const v = value as { version?: unknown; answered?: unknown };
  return v.version === 1 && typeof v.answered === "object" && v.answered !== null;
}

export async function getProgress(topicId: string): Promise<TopicProgress> {
  const cached = cache.get(topicId);
  if (cached) return cached;
  const pending = inflight.get(topicId);
  if (pending) return pending;

  const req = (async () => {
    try {
      const res = await fetch(`/api/progress/${encodeURIComponent(topicId)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as unknown;
      const p = isTopicProgress(data) ? data : empty();
      cache.set(topicId, p);
      return p;
    } catch (err) {
      console.warn("[progress] fallo al leer del servidor:", err);
      const p = empty();
      cache.set(topicId, p);
      return p;
    } finally {
      inflight.delete(topicId);
    }
  })();
  inflight.set(topicId, req);
  return req;
}

export async function markAnswered(
  topicId: string,
  questionId: string,
  correct: boolean
): Promise<void> {
  const current = cache.get(topicId) ?? (await getProgress(topicId));
  // Actualización optimista: la UI ve el cambio sin esperar al servidor.
  current.answered[questionId] = { correct, at: new Date().toISOString() };
  cache.set(topicId, current);

  try {
    const res = await fetch(`/api/progress/${encodeURIComponent(topicId)}/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ questionId, correct }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const updated = (await res.json()) as unknown;
    if (isTopicProgress(updated)) cache.set(topicId, updated);
  } catch (err) {
    console.warn("[progress] no s'ha pogut desar al servidor:", err);
  }
}

export async function resetTopic(topicId: string): Promise<void> {
  cache.delete(topicId);
  try {
    await fetch(`/api/progress/${encodeURIComponent(topicId)}`, { method: "DELETE" });
  } catch (err) {
    console.warn("[progress] no s'ha pogut esborrar al servidor:", err);
  }
}

export async function countStats(
  topicId: string
): Promise<{ done: number; correct: number; wrong: number }> {
  const p = await getProgress(topicId);
  let correct = 0;
  let wrong = 0;
  for (const k in p.answered) {
    if (p.answered[k].correct) correct++;
    else wrong++;
  }
  return { done: correct + wrong, correct, wrong };
}
