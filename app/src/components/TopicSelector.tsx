import { useEffect, useState } from "react";
import type { TopicIndexEntry } from "../types";
import { loadIndex, loadTopic } from "../data/loadTopics";
import { countStats, resetTopic } from "../data/progress";
import { t } from "../i18n";

type Props = {
  onPick: (entry: TopicIndexEntry) => void;
};

type Row = TopicIndexEntry & { done: number; correct: number; wrong: number; total: number };

export function TopicSelector({ onPick }: Props) {
  const [rows, setRows] = useState<Row[] | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const refresh = async () => {
    try {
      const idx = await loadIndex();
      const enriched = await Promise.all(
        idx.topics.map(async (e) => {
          let total = 0;
          try {
            const topic = await loadTopic(e.file);
            total = topic.questions.length;
          } catch {
            // si falla, mostramos 0 y el error saldrá al entrar en el tema
          }
          const s = await countStats(e.id);
          return { ...e, done: s.done, correct: s.correct, wrong: s.wrong, total };
        })
      );
      setRows(enriched);
    } catch (e) {
      setErr(String(e));
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  if (err) return <p className="text-rose-700">{t.errorLoading}</p>;
  if (!rows) return <p className="text-slate-500">{t.loading}</p>;

  return (
    <section className="mx-auto max-w-2xl">
      <h2 className="mb-4 text-lg font-semibold text-slate-700">{t.chooseTopic}</h2>
      <ul className="space-y-3">
        {rows.map((r) => {
          const completed = r.total > 0 && r.done >= r.total;
          return (
            <li key={r.id}>
              <div className="flex items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <button type="button" onClick={() => onPick(r)} className="flex-1 text-left">
                  <div className="text-base font-semibold text-slate-900">{r.name}</div>
                  <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-500">
                    <span>{t.progress(r.done, r.total)}</span>
                    {r.done > 0 && (
                      <span className="inline-flex items-center gap-2">
                        <span className="inline-flex items-center gap-1 rounded-md bg-emerald-50 px-1.5 py-0.5 text-emerald-700">
                          ✓ {r.correct}
                        </span>
                        <span className="inline-flex items-center gap-1 rounded-md bg-rose-50 px-1.5 py-0.5 text-rose-700">
                          ✗ {r.wrong}
                        </span>
                      </span>
                    )}
                    {completed && <span className="text-emerald-700">· completat ✓</span>}
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    if (confirm(t.resetConfirm(r.name))) {
                      void resetTopic(r.id).then(() => refresh());
                    }
                  }}
                  className="rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-100"
                  title={t.reset}
                >
                  {t.reset}
                </button>
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
