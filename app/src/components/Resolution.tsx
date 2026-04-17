import { BlockMath } from "react-katex";
import type { Step } from "../types";
import { RichText } from "./RichText";
import { GraphicView } from "./GraphicView";
import { t } from "../i18n";

export function Resolution({ steps }: { steps: Step[] }) {
  return (
    <section className="mt-6 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="mb-3 text-base font-semibold text-slate-700">{t.resolution}</h3>
      <ol className="space-y-3">
        {steps.map((s, i) => (
          <li key={i} className="flex gap-3">
            <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-semibold text-slate-600">
              {i + 1}
            </span>
            <div className="flex-1 leading-relaxed text-slate-800">
              {s.kind === "text" && <RichText text={s.text} />}
              {s.kind === "math" && (
                <div className="overflow-x-auto">
                  <BlockMath math={s.tex} />
                </div>
              )}
              {s.kind === "graphic" && <GraphicView graphic={s.graphic} size={300} />}
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
