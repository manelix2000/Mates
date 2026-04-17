import { Fragment, useMemo } from "react";
import type { VectorPlotGraphic } from "../types";

type Props = {
  graphic: VectorPlotGraphic;
  size?: number; // base pixel size, scales with viewBox
};

const axisColor = "#64748b";
const gridColor = "#e2e8f0";
const pointColor = "#111827";

export function VectorPlot({ graphic, size = 360 }: Props) {
  const { xRange, yRange, gridStep = 1, points = [], vectors = [] } = graphic;

  const [xmin, xmax] = xRange;
  const [ymin, ymax] = yRange;
  const w = xmax - xmin;
  const h = ymax - ymin;
  const pad = 18; // padding in user units scaled via viewBox
  const scale = size / Math.max(w, h);
  const width = Math.max(240, w * scale + pad * 2);
  const height = Math.max(240, h * scale + pad * 2);

  // transform (math coords → svg coords)
  const X = (x: number) => pad + (x - xmin) * scale;
  const Y = (y: number) => pad + (ymax - y) * scale;

  const gridLines = useMemo(() => {
    const lines: { x1: number; y1: number; x2: number; y2: number; key: string }[] = [];
    for (let x = Math.ceil(xmin / gridStep) * gridStep; x <= xmax; x += gridStep) {
      lines.push({ x1: X(x), y1: Y(ymin), x2: X(x), y2: Y(ymax), key: `vx${x}` });
    }
    for (let y = Math.ceil(ymin / gridStep) * gridStep; y <= ymax; y += gridStep) {
      lines.push({ x1: X(xmin), y1: Y(y), x2: X(xmax), y2: Y(y), key: `hy${y}` });
    }
    return lines;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [xmin, xmax, ymin, ymax, gridStep, scale]);

  const markerIds = vectors.map((_, i) => `arrow-${i}`);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      style={{ maxWidth: width, height: "auto", display: "block" }}
      className="mx-auto"
      role="img"
      aria-label="Representació gràfica de vectors"
    >
      <defs>
        {vectors.map((v, i) => (
          <marker
            key={markerIds[i]}
            id={markerIds[i]}
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="7"
            markerHeight="7"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" fill={v.color ?? "#d33"} />
          </marker>
        ))}
      </defs>

      {/* grid */}
      <g>
        {gridLines.map((l) => (
          <line
            key={l.key}
            x1={l.x1}
            y1={l.y1}
            x2={l.x2}
            y2={l.y2}
            stroke={gridColor}
            strokeWidth={1}
          />
        ))}
      </g>

      {/* axes */}
      {ymin <= 0 && ymax >= 0 && (
        <line x1={X(xmin)} y1={Y(0)} x2={X(xmax)} y2={Y(0)} stroke={axisColor} strokeWidth={1.5} />
      )}
      {xmin <= 0 && xmax >= 0 && (
        <line x1={X(0)} y1={Y(ymin)} x2={X(0)} y2={Y(ymax)} stroke={axisColor} strokeWidth={1.5} />
      )}

      {/* unit ticks labels (only at 1 and on axis) */}
      {xmin <= 0 && xmax >= 0 && ymin <= 1 && ymax >= 1 && (
        <text x={X(0) - 6} y={Y(1) + 4} fontSize="11" fill={axisColor} textAnchor="end">
          1
        </text>
      )}
      {ymin <= 0 && ymax >= 0 && xmin <= 1 && xmax >= 1 && (
        <text x={X(1)} y={Y(0) + 14} fontSize="11" fill={axisColor} textAnchor="middle">
          1
        </text>
      )}

      {/* vectors */}
      <g>
        {vectors.map((v, i) => {
          const color = v.color ?? "#d33";
          const x1 = X(v.from[0]);
          const y1 = Y(v.from[1]);
          const x2 = X(v.to[0]);
          const y2 = Y(v.to[1]);
          const mx = (x1 + x2) / 2;
          const my = (y1 + y2) / 2;
          return (
            <Fragment key={`v${i}`}>
              <line
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke={color}
                strokeWidth={2.4}
                strokeDasharray={v.dashed ? "5,4" : undefined}
                markerEnd={`url(#${markerIds[i]})`}
              />
              {v.label && (
                <text
                  x={mx + 8}
                  y={my - 6}
                  fontSize="13"
                  fontStyle="italic"
                  fill={color}
                  fontWeight={600}
                >
                  {v.label}
                </text>
              )}
            </Fragment>
          );
        })}
      </g>

      {/* points */}
      <g>
        {points.map((p, i) => {
          const cx = X(p.at[0]);
          const cy = Y(p.at[1]);
          return (
            <Fragment key={`p${i}`}>
              <circle cx={cx} cy={cy} r={3} fill={pointColor} />
              <text x={cx + 6} y={cy - 6} fontSize="13" fontWeight={600} fill={pointColor}>
                {p.label}
              </text>
            </Fragment>
          );
        })}
      </g>
    </svg>
  );
}
