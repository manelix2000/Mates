import type { RightTriangleGraphic } from "../types";

type Props = {
  graphic: RightTriangleGraphic;
  size?: number;
};

const strokeColor = "#475569";
const fillColor = "#fce7f3";
const altitudeColor = "#94a3b8";
const labelColor = "#0f172a";
const highlightColor = "#be185d";

export function RightTrianglePlot({ graphic, size = 360 }: Props) {
  const { b, c, labels = {}, showAltitude = true, highlight = [] } = graphic;

  const pad = 48;
  const maxDim = Math.max(b, c);
  const scale = (size - 2 * pad) / maxDim;

  const width = b * scale + 2 * pad;
  const height = c * scale + 2 * pad;

  const Ax = pad;
  const Ay = height - pad;
  const Bx = pad;
  const By = height - pad - c * scale;
  const Cx = pad + b * scale;
  const Cy = height - pad;

  const a2 = b * b + c * c;
  const Hx = Ax + (b * c * c) / a2 * scale;
  const Hy = Ay - (c * b * b) / a2 * scale;

  const hl = (key: "a" | "b" | "c" | "h" | "m" | "n") =>
    highlight.includes(key) ? highlightColor : labelColor;
  const hlStroke = (key: "a" | "b" | "c" | "h" | "m" | "n") =>
    highlight.includes(key) ? highlightColor : strokeColor;

  const rightAngleSize = Math.min(14, Math.min(b, c) * scale * 0.2);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      style={{ maxWidth: size + 40, height: "auto", display: "block", margin: "0 auto" }}
      role="img"
      aria-label="Triangle rectangle"
    >
      <polygon
        points={`${Ax},${Ay} ${Bx},${By} ${Cx},${Cy}`}
        fill={fillColor}
        stroke={strokeColor}
        strokeWidth={1.5}
      />

      <line x1={Ax} y1={Ay} x2={Bx} y2={By} stroke={hlStroke("c")} strokeWidth={highlight.includes("c") ? 3 : 1.5} />
      <line x1={Ax} y1={Ay} x2={Cx} y2={Cy} stroke={hlStroke("b")} strokeWidth={highlight.includes("b") ? 3 : 1.5} />
      <line x1={Bx} y1={By} x2={Cx} y2={Cy} stroke={hlStroke("a")} strokeWidth={highlight.includes("a") ? 3 : 1.5} />

      <polyline
        points={`${Ax + rightAngleSize},${Ay} ${Ax + rightAngleSize},${Ay - rightAngleSize} ${Ax},${Ay - rightAngleSize}`}
        fill="none"
        stroke={strokeColor}
        strokeWidth={1}
      />

      {showAltitude && (
        <>
          <line
            x1={Ax}
            y1={Ay}
            x2={Hx}
            y2={Hy}
            stroke={hlStroke("h")}
            strokeWidth={highlight.includes("h") ? 2.5 : 1.5}
            strokeDasharray="5,4"
          />
          {highlight.includes("m") || labels.m ? (
            <circle cx={Hx} cy={Hy} r={2.5} fill={altitudeColor} />
          ) : null}
        </>
      )}

      <LabelPoint x={Ax} y={Ay} dx={-14} dy={18} text={labels.A ?? "A"} />
      <LabelPoint x={Bx} y={By} dx={-14} dy={-6} text={labels.B ?? "B"} />
      <LabelPoint x={Cx} y={Cy} dx={12} dy={18} text={labels.C ?? "C"} />

      {labels.c !== undefined && (
        <SideLabel
          x={(Ax + Bx) / 2}
          y={(Ay + By) / 2}
          dx={-12}
          dy={4}
          anchor="end"
          text={labels.c}
          color={hl("c")}
          bold={highlight.includes("c")}
        />
      )}
      {labels.b !== undefined && (
        <SideLabel
          x={(Ax + Cx) / 2}
          y={(Ay + Cy) / 2}
          dx={0}
          dy={22}
          anchor="middle"
          text={labels.b}
          color={hl("b")}
          bold={highlight.includes("b")}
        />
      )}
      {labels.a !== undefined && (
        <SideLabel
          x={(Bx + Cx) / 2}
          y={(By + Cy) / 2}
          dx={14}
          dy={-8}
          anchor="start"
          text={labels.a}
          color={hl("a")}
          bold={highlight.includes("a")}
        />
      )}

      {showAltitude && labels.h !== undefined && (
        <SideLabel
          x={(Ax + Hx) / 2}
          y={(Ay + Hy) / 2}
          dx={8}
          dy={4}
          anchor="start"
          text={labels.h}
          color={hl("h")}
          bold={highlight.includes("h")}
        />
      )}
      {showAltitude && labels.m !== undefined && (
        <SideLabel
          x={(Bx + Hx) / 2}
          y={(By + Hy) / 2}
          dx={10}
          dy={-4}
          anchor="start"
          text={labels.m}
          color={hl("m")}
          bold={highlight.includes("m")}
        />
      )}
      {showAltitude && labels.n !== undefined && (
        <SideLabel
          x={(Hx + Cx) / 2}
          y={(Hy + Cy) / 2}
          dx={10}
          dy={-4}
          anchor="start"
          text={labels.n}
          color={hl("n")}
          bold={highlight.includes("n")}
        />
      )}
    </svg>
  );
}

function LabelPoint({
  x,
  y,
  dx,
  dy,
  text,
}: {
  x: number;
  y: number;
  dx: number;
  dy: number;
  text: string;
}) {
  return (
    <text
      x={x + dx}
      y={y + dy}
      fontSize={14}
      fontWeight={700}
      fill={labelColor}
      textAnchor="middle"
    >
      {text}
    </text>
  );
}

function SideLabel({
  x,
  y,
  dx,
  dy,
  anchor,
  text,
  color,
  bold,
}: {
  x: number;
  y: number;
  dx: number;
  dy: number;
  anchor: "start" | "middle" | "end";
  text: string;
  color: string;
  bold?: boolean;
}) {
  return (
    <text
      x={x + dx}
      y={y + dy}
      fontSize={13}
      fontWeight={bold ? 700 : 500}
      fill={color}
      textAnchor={anchor}
      style={{ paintOrder: "stroke", stroke: "white", strokeWidth: 3, strokeLinejoin: "round" }}
    >
      {text}
    </text>
  );
}
