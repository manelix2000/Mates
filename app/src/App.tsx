import { useEffect, useMemo, useState } from "react";
import type { Question, Topic, TopicIndexEntry } from "./types";
import { loadTopic } from "./data/loadTopics";
import { getProgress, markAnswered, resetTopic } from "./data/progress";
import { TopicSelector } from "./components/TopicSelector";
import { QuestionView } from "./components/QuestionView";
import { TopicCompleted } from "./components/TopicCompleted";
import { t } from "./i18n";

type State =
  | { kind: "selecting" }
  | { kind: "loading"; entry: TopicIndexEntry }
  | { kind: "error"; message: string }
  | { kind: "playing"; topic: Topic; queue: Question[]; idx: number }
  | { kind: "completed"; topic: Topic };

function buildQueue(topic: Topic, answered: Record<string, unknown>): Question[] {
  const pending = topic.questions.filter((q) => !answered[q.id]);
  return shuffle(pending);
}

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export function App() {
  const [state, setState] = useState<State>({ kind: "selecting" });

  useEffect(() => {
    if (state.kind !== "loading") return;
    let cancelled = false;
    (async () => {
      try {
        const topic = await loadTopic(state.entry.file);
        const progress = await getProgress(topic.id);
        if (cancelled) return;
        const queue = buildQueue(topic, progress.answered);
        if (queue.length === 0) setState({ kind: "completed", topic });
        else setState({ kind: "playing", topic, queue, idx: 0 });
      } catch (e) {
        if (!cancelled) setState({ kind: "error", message: String(e) });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [state]);

  const title = useMemo(() => t.appTitle, []);

  const backToSelect = () => setState({ kind: "selecting" });

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-4">
          <h1 className="text-lg font-bold text-slate-900">{title}</h1>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-6">
        {state.kind === "selecting" && (
          <TopicSelector onPick={(entry) => setState({ kind: "loading", entry })} />
        )}

        {state.kind === "loading" && <p className="text-slate-500">{t.loading}</p>}

        {state.kind === "error" && (
          <div className="rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
            <p className="font-semibold">{t.errorLoading}</p>
            <p className="mt-1 text-sm">{state.message}</p>
            <button
              type="button"
              onClick={backToSelect}
              className="mt-3 rounded-md bg-white px-3 py-1.5 text-sm text-slate-700 shadow"
            >
              {t.back}
            </button>
          </div>
        )}

        {state.kind === "playing" && (
          <QuestionView
            question={state.queue[state.idx]}
            index={state.idx}
            total={state.queue.length}
            onAnswered={(correct) =>
              void markAnswered(state.topic.id, state.queue[state.idx].id, correct)
            }
            onNext={() => {
              const next = state.idx + 1;
              if (next >= state.queue.length) {
                setState({ kind: "completed", topic: state.topic });
              } else {
                setState({ ...state, idx: next });
              }
            }}
            onBack={backToSelect}
          />
        )}

        {state.kind === "completed" && (
          <TopicCompleted
            topicName={state.topic.name}
            onBack={backToSelect}
            onRestart={() => {
              void resetTopic(state.topic.id);
              const queue = shuffle(state.topic.questions);
              setState({ kind: "playing", topic: state.topic, queue, idx: 0 });
            }}
          />
        )}
      </main>

      <footer className="py-8 text-center text-xs text-slate-400">
        Mates 4t ESO · pràctica local
      </footer>
    </div>
  );
}
