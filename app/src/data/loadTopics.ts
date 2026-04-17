import type { Topic, TopicIndex } from "../types";

const BASE = `${import.meta.env.BASE_URL}topics/`;

export async function loadIndex(): Promise<TopicIndex> {
  const res = await fetch(`${BASE}index.json`, { cache: "no-cache" });
  if (!res.ok) throw new Error(`index.json: ${res.status}`);
  return res.json();
}

export async function loadTopic(file: string): Promise<Topic> {
  const res = await fetch(`${BASE}${file}`, { cache: "no-cache" });
  if (!res.ok) throw new Error(`${file}: ${res.status}`);
  const data = (await res.json()) as Topic;
  if (!data.questions || !Array.isArray(data.questions)) {
    throw new Error(`${file}: formato inválido (questions)`);
  }
  return data;
}
