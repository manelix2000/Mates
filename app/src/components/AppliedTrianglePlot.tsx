import type { AppliedTriangleGraphic } from "../types";

type Props = {
  graphic: AppliedTriangleGraphic;
  size?: number;
};

const strokeColor = "#475569";
const fillColor = "#fce7f3";
const labelColor = "#0f172a";
const highlightColor = "#be185d";
const angleColor = "#2563eb";

export function AppliedTrianglePlot({ graphic, size = 420 }: Props) {
  const { angleDeg, labels = {}, vertexLabels = {}, highlight = [] } = graphic;

  const clamped = Math.max(10, Math.min(80, angleDeg));
  const rad = (clamped * Math.PI) / 180;

  const pad = 56;
  const drawW = size - 2 * pad;
  const drawH = size * 0.62 - 2 * pad;

  let base: number;
  let alt: number;
  if (Math.tan(rad) >= drawH / drawW) {
    alt = drawH;
    base = drawH / Math.tan(rad);
  } else {
    base = drawW;
    alt = drawW * Math.tan(rad);
  }

  const width = base + 2 * pad;
  const height = alt + 2 * pad;

  const Ax = pad;
  const Ay = height - pad;
  const Bx = pad + base;
  const By = height - pad;
  const Cx = pad + base;
  const Cy = height - pad - alt;

  const hl = (k: "opposite" | "adjacent" | "hypotenuse") =>
    highlight.includes(k) ? highlightColor : labelColor;
  const hlStroke = (k: "opposite" | "adjacent" | "hypotenuse") =>
    highlight.includes(k) ? highlightColor : strokeColor;
  const widthOf = (k: "opposite" | "adjacent" | "hypotenuse") =>
    highlight.includes(k) ? 3 : 1.8;

  const raSize = 14;

  const arcR = Math.min(46, base * 0.32);
  const arcEndX = Ax + arcR * Math.cos(rad);
  const arcEndY = Ay - arcR * Math.sin(rad);
  const arcPath = `M ${Ax + arcR} ${Ay} A ${arcR} ${arcR} 0 0 0 ${arcEndX} ${arcEndY}`;

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      style={{ maxWidth: size + 40, height: "auto", display: "block", margin: "0 auto" }}
      role="img"
      aria-label="Triangle rectangle aplicat"
    >
      <polygon
        points={`${Ax},${Ay} ${Bx},${By} ${Cx},${Cy}`}
        fill={fillColor}
        stroke={strokeColor}
        strokeWidth={1.5}
      />

      <line x1={Ax} y1={Ay} x2={Bx} y2={By} stroke={hlStroke("adjacent")} strokeWidth={widthOf("adjacent")} />
      <line x1={Bx} y1={By} x2={Cx} y2={Cy} stroke={hlStroke("opposite")} strokeWidth={widthOf("opposite")} />
      <line x1={Ax} y1={Ay} x2={Cx} y2={Cy} stroke={hlStroke("hypotenuse")} strokeWidth={widthOf("hypotenuse")} />

      <polyline
        points={`${Bx - raSize},${By} ${Bx - raSize},${By - raSize} ${Bx},${By - raSize}`}
        fill="none"
        stroke={strokeColor}
        strokeWidth={1}
      />

      <path d={arcPath} fill="none" stroke={angleColor} strokeWidth={1.5} />
      {labels.angle !== undefined && (
        <SvgText
          x={Ax + arcR * 0.65 * Math.cos(rad / 2) + 6}
          y={Ay - arcR * 0.65 * Math.sin(rad / 2) + 4}
          anchor="start"
          fontSize={14}
          color={angleColor}
          bold
          text={labels.angle}
        />
      )}

      {vertexLabels.acuteAngle && (
        <SvgText x={Ax - 6} y={Ay + 22} anchor="end" fontSize={13} color={labelColor} text={vertexLabels.acuteAngle} />
      )}
      {vertexLabels.rightAngle && (
        <SvgText x={Bx + 6} y={By + 22} anchor="start" fontSize={13} color={labelColor} text={vertexLabels.rightAngle} />
      )}
      {vertexLabels.top && (
        <SvgText x={Cx + 6} y={Cy - 8} anchor="start" fontSize={13} color={labelColor} text={vertexLabels.top} />
      )}

      {labels.adjacent !== undefined && (
        <SvgText
          x={(Ax + Bx) / 2}
          y={By + 40}
          anchor="middle"
          fontSize={14}
          color={hl("adjacent")}
          bold={highlight.includes("adjacent")}
          text={labels.adjacent}
        />
      )}
      {labels.opposite !== undefined && (
        <SvgText
          x={Bx + 14}
          y={(By + Cy) / 2 + 4}
          anchor="start"
          fontSize={14}
          color={hl("opposite")}
          bold={highlight.includes("opposite")}
          text={labels.opposite}
        />
      )}
      {labels.hypotenuse !== undefined && (
        <SvgText
          x={(Ax + Cx) / 2 - 16}
          y={(Ay + Cy) / 2 - 6}
          anchor="end"
          fontSize={14}
          color={hl("hypotenuse")}
          bold={highlight.includes("hypotenuse")}
          text={labels.hypotenuse}
        />
      )}
    </svg>
  );
}

function SvgText({
  x,
  y,
  anchor,
  fontSize,
  color,
  bold,
  text,
}: {
  x: number;
  y: number;
  anchor: "start" | "middle" | "end";
  fontSize: number;
  color: string;
  bold?: boolean;
  text: string;
}) {
  return (
    <text
      x={x}
      y={y}
      fontSize={fontSize}
      fontWeight={bold ? 700 : 500}
      fill={color}
      textAnchor={anchor}
      stroke="#ffffff"
      strokeWidth={3}
      paintOrder="stroke"
    >
      {text}
    </text>
  );
}
