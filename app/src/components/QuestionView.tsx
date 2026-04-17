import { useState } from "react";
import type { Question } from "../types";
import { t } from "../i18n";
import { RichText } from "./RichText";
import { GraphicView } from "./GraphicView";
import { OptionList } from "./OptionList";
import { Resolution } from "./Resolution";

type Props = {
  question: Question;
  index: number;
  total: number;
  onAnswered: (correct: boolean) => void;
  onNext: () => void;
  onBack: () => void;
};

export function QuestionView({ question, index, total, onAnswered, onNext, onBack }: Props) {
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const isCorrect = selected !== null && selected === question.correct;

  const onCheck = () => {
    if (selected === null) return;
    setRevealed(true);
    onAnswered(selected === question.correct);
  };

  const onNextClick = () => {
    setSelected(null);
    setRevealed(false);
    onNext();
  };

  return (
    <article className="mx-auto max-w-3xl">
      <header className="mb-4 flex items-center justify-between">
        <button
          type="button"
          onClick={onBack}
          className="text-sm text-slate-500 underline-offset-2 hover:underline"
        >
          ← {t.back}
        </button>
        <span className="text-sm font-medium text-slate-500">
          {index + 1} / {total}
        </span>
      </header>

      <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
        <p className="text-lg leading-relaxed text-slate-900">
          <RichText text={question.statement} />
        </p>

        {question.graphic && (
          <div className="mt-4 rounded-lg bg-slate-50 p-3">
            <GraphicView graphic={question.graphic} />
          </div>
        )}

        <OptionList
          options={question.options}
          selected={selected}
          correct={question.correct}
          revealed={revealed}
          onSelect={(i) => !revealed && setSelected(i)}
        />

        {!revealed ? (
          <div className="mt-5 flex items-center justify-between">
            <span className="text-sm text-slate-500">
              {selected === null ? t.noOptionSelected : ""}
            </span>
            <button
              type="button"
              onClick={onCheck}
              disabled={selected === null}
              className="inline-flex items-center rounded-lg bg-sky-600 px-5 py-2.5 font-semibold text-white shadow hover:bg-sky-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {t.check}
            </button>
          </div>
        ) : (
          <div className="mt-5 flex flex-col gap-3">
            <div
              className={`rounded-lg px-4 py-3 font-semibold ${
                isCorrect
                  ? "bg-emerald-100 text-emerald-800"
                  : "bg-rose-100 text-rose-800"
              }`}
            >
              {isCorrect ? `✓ ${t.correct}` : `✗ ${t.incorrect}`}
              {!isCorrect && (
                <div className="mt-1 text-sm font-normal text-rose-900">
                  {t.correctAnswerPrefix}
                  <RichText text={question.options[question.correct]} />
                  {t.correctAnswerSuffix}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {revealed && <Resolution steps={question.resolution} />}

      {revealed && (
        <div className="mt-5 flex justify-end">
          <button
            type="button"
            onClick={onNextClick}
            className="inline-flex items-center rounded-lg bg-slate-900 px-5 py-2.5 font-semibold text-white shadow hover:bg-slate-800"
          >
            {t.next} →
          </button>
        </div>
      )}
    </article>
  );
}
