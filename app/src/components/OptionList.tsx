import { RichText } from "./RichText";

type Props = {
  options: string[];
  selected: number | null;
  correct: number;
  revealed: boolean;
  onSelect: (i: number) => void;
};

export function OptionList({ options, selected, correct, revealed, onSelect }: Props) {
  return (
    <ul className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
      {options.map((opt, i) => {
        const isSelected = selected === i;
        const isCorrect = i === correct;
        let classes =
          "flex w-full items-center gap-3 rounded-lg border px-4 py-3 text-left transition focus:outline-none focus:ring-2 focus:ring-sky-400";
        if (!revealed) {
          classes += isSelected
            ? " border-sky-500 bg-sky-50"
            : " border-slate-200 bg-white hover:border-slate-400";
        } else {
          if (isCorrect) classes += " border-emerald-500 bg-emerald-50";
          else if (isSelected) classes += " border-rose-500 bg-rose-50";
          else classes += " border-slate-200 bg-white opacity-70";
        }
        return (
          <li key={i}>
            <button
              type="button"
              disabled={revealed}
              onClick={() => onSelect(i)}
              className={classes}
            >
              <span className="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-700">
                {String.fromCharCode(65 + i)}
              </span>
              <span className="text-base text-slate-800">
                <RichText text={opt} />
              </span>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
