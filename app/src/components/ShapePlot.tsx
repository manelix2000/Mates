import type { ShapePlotGraphic, ShapePiece, ShapeLabel } from "../types";

type Props = {
  graphic: ShapePlotGraphic;
  size?: number;
};

const strokeColor = "#475569";
const fillColor = "#fce7f3";
const highlightStroke = "#be185d";
const highlightFill = "#fbcfe8";
const labelColor = "#0f172a";
const highlightLabelColor = "#be185d";
const mutedLabelColor = "#64748b";

export function ShapePlot({ graphic, size = 420 }: Props) {
  // Calculamos un viewBox ajustado a las primitivas reales (ignorando el
  // padding excesivo que pueda venir del generador) para que la figura
  // ocupe el máximo espacio posible.
  const bounds = computeBounds(graphic.shapes);
  const fallback = graphic.viewBox;
  const baseUnit = Math.max(
    bounds ? Math.max(bounds.w, bounds.h) : Math.max(fallback[2], fallback[3]),
    1,
  );
  // Padding suficiente para alojar las etiquetas exteriores (típicamente
  // colocadas a ~1 unidad fuera de la figura) y un poco de aire.
  const pad = baseUnit * 0.18;

  const x = bounds ? bounds.x - pad : fallback[0] - pad;
  const y = bounds ? bounds.y - pad : fallback[1] - pad;
  const w = bounds ? bounds.w + 2 * pad : fallback[2] + 2 * pad;
  const h = bounds ? bounds.h + 2 * pad : fallback[3] + 2 * pad;

  const unit = Math.max(w, h);
  // Letra más discreta: ~3,2 % del lado mayor del viewBox.
  const labelFontSize = unit * 0.032;
  const strokeScale = unit / 320;

  return (
    <svg
      viewBox={`${x} ${y} ${w} ${h}`}
      width="100%"
      style={{ maxWidth: size + 40, height: "auto", display: "block", margin: "0 auto" }}
      role="img"
      aria-label="Figura geomètrica"
    >
      {graphic.shapes.map((piece, i) => (
        <ShapePieceView key={i} piece={piece} strokeScale={strokeScale} />
      ))}
      {(graphic.labels ?? []).map((l, i) => (
        <LabelView key={i} label={l} fontSize={labelFontSize} />
      ))}
    </svg>
  );
}

function computeBounds(shapes: ShapePiece[]): { x: number; y: number; w: number; h: number } | null {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  const upd = (px: number, py: number) => {
    if (px < minX) minX = px;
    if (py < minY) minY = py;
    if (px > maxX) maxX = px;
    if (py > maxY) maxY = py;
  };
  for (const s of shapes) {
    if (s.type === "polygon") {
      for (const p of s.points) upd(p[0], p[1]);
    } else if (s.type === "circle") {
      upd(s.center[0] - s.r, s.center[1] - s.r);
      upd(s.center[0] + s.r, s.center[1] + s.r);
    } else if (s.type === "arc") {
      // Aproximación: la caja del círculo completo es siempre un superconjunto
      // de la del arco; suficiente para dimensionar el viewBox.
      upd(s.center[0] - s.r, s.center[1] - s.r);
      upd(s.center[0] + s.r, s.center[1] + s.r);
    } else if (s.type === "line") {
      upd(s.from[0], s.from[1]);
      upd(s.to[0], s.to[1]);
    }
  }
  if (!isFinite(minX)) return null;
  return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
}

function strokeOf(piece: { highlight?: boolean }) {
  return piece.highlight ? highlightStroke : strokeColor;
}
function fillOf(piece: { highlight?: boolean; filled?: boolean }) {
  if (!piece.filled) return "none";
  return piece.highlight ? highlightFill : fillColor;
}
function dashOf(piece: { dashed?: boolean }, scale: number) {
  if (!piece.dashed) return undefined;
  const a = Math.max(2, 6 * scale);
  const b = Math.max(1.5, 4 * scale);
  return `${a} ${b}`;
}
function widthOf(piece: { highlight?: boolean }, scale: number) {
  const base = piece.highlight ? 2.4 : 1.6;
  return base * scale;
}

function ShapePieceView({ piece, strokeScale }: { piece: ShapePiece; strokeScale: number }) {
  if (piece.type === "polygon") {
    return (
      <polygon
        points={piece.points.map((p) => `${p[0]},${p[1]}`).join(" ")}
        fill={fillOf(piece)}
        stroke={strokeOf(piece)}
        strokeWidth={widthOf(piece, strokeScale)}
        strokeDasharray={dashOf(piece, strokeScale)}
        strokeLinejoin="round"
      />
    );
  }
  if (piece.type === "circle") {
    return (
      <circle
        cx={piece.center[0]}
        cy={piece.center[1]}
        r={piece.r}
        fill={fillOf(piece)}
        stroke={strokeOf(piece)}
        strokeWidth={widthOf(piece, strokeScale)}
        strokeDasharray={dashOf(piece, strokeScale)}
      />
    );
  }
  if (piece.type === "arc") {
    const { center, r, fromDeg, toDeg, closed } = piece;
    const a0 = (fromDeg * Math.PI) / 180;
    const a1 = (toDeg * Math.PI) / 180;
    const p0 = [center[0] + r * Math.cos(a0), center[1] + r * Math.sin(a0)];
    const p1 = [center[0] + r * Math.cos(a1), center[1] + r * Math.sin(a1)];
    const large = Math.abs(toDeg - fromDeg) > 180 ? 1 : 0;
    const sweep = toDeg > fromDeg ? 1 : 0;
    let d = `M ${p0[0]} ${p0[1]} A ${r} ${r} 0 ${large} ${sweep} ${p1[0]} ${p1[1]}`;
    if (closed) {
      d += ` L ${center[0]} ${center[1]} Z`;
    }
    return (
      <path
        d={d}
        fill={fillOf(piece)}
        stroke={strokeOf(piece)}
        strokeWidth={widthOf(piece, strokeScale)}
        strokeDasharray={dashOf(piece, strokeScale)}
      />
    );
  }
  // line
  return (
    <line
      x1={piece.from[0]}
      y1={piece.from[1]}
      x2={piece.to[0]}
      y2={piece.to[1]}
      stroke={strokeOf(piece)}
      strokeWidth={widthOf(piece, strokeScale)}
      strokeDasharray={dashOf(piece, strokeScale)}
    />
  );
}

function LabelView({ label, fontSize }: { label: ShapeLabel; fontSize: number }) {
  const color =
    label.color === "highlight"
      ? highlightLabelColor
      : label.color === "muted"
      ? mutedLabelColor
      : labelColor;
  const anchor = label.anchor ?? "middle";
  return (
    <text
      x={label.at[0]}
      y={label.at[1]}
      fontSize={fontSize}
      fontWeight={label.bold ? 700 : 500}
      fill={color}
      textAnchor={anchor}
      stroke="#ffffff"
      strokeWidth={fontSize * 0.22}
      paintOrder="stroke"
      dominantBaseline="middle"
    >
      {label.text}
    </text>
  );
}
