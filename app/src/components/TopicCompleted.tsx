import { t } from "../i18n";

type Props = {
  topicName: string;
  onRestart: () => void;
  onBack: () => void;
};

export function TopicCompleted({ topicName, onRestart, onBack }: Props) {
  return (
    <section className="mx-auto max-w-xl rounded-2xl border border-emerald-200 bg-emerald-50 p-8 text-center shadow-sm">
      <div className="text-5xl">🎉</div>
      <h2 className="mt-3 text-xl font-bold text-emerald-900">{t.allDoneTitle}</h2>
      <p className="mt-2 text-emerald-800">{t.allDoneBody}</p>
      <p className="mt-1 text-sm text-emerald-700">({topicName})</p>
      <div className="mt-6 flex justify-center gap-3">
        <button
          type="button"
          onClick={onBack}
          className="rounded-lg border border-slate-300 bg-white px-5 py-2.5 font-semibold text-slate-700 hover:bg-slate-50"
        >
          {t.back}
        </button>
        <button
          type="button"
          onClick={() => {
            if (confirm(t.resetConfirm(topicName))) onRestart();
          }}
          className="rounded-lg bg-emerald-600 px-5 py-2.5 font-semibold text-white shadow hover:bg-emerald-700"
        >
          {t.restart}
        </button>
      </div>
    </section>
  );
}
