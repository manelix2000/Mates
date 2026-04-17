import { InlineMath } from "react-katex";

/**
 * Renderiza texto que puede contener fórmulas inline delimitadas por $...$.
 * Las fórmulas se pasan a KaTeX; el resto es texto plano.
 */
export function RichText({ text }: { text: string }) {
  const parts = splitByDollarMath(text);
  return (
    <span>
      {parts.map((p, i) =>
        p.kind === "math" ? <InlineMath key={i} math={p.content} /> : <span key={i}>{p.content}</span>
      )}
    </span>
  );
}

type Part = { kind: "text" | "math"; content: string };

function splitByDollarMath(input: string): Part[] {
  const parts: Part[] = [];
  let i = 0;
  let buf = "";
  while (i < input.length) {
    const c = input[i];
    if (c === "\\" && input[i + 1] === "$") {
      buf += "$";
      i += 2;
      continue;
    }
    if (c === "$") {
      if (buf) {
        parts.push({ kind: "text", content: buf });
        buf = "";
      }
      const end = input.indexOf("$", i + 1);
      if (end === -1) {
        buf += input.slice(i);
        break;
      }
      parts.push({ kind: "math", content: input.slice(i + 1, end) });
      i = end + 1;
      continue;
    }
    buf += c;
    i++;
  }
  if (buf) parts.push({ kind: "text", content: buf });
  return parts;
}
