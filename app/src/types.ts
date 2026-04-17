export type Vec2 = [number, number];

export type GraphicPoint = { label: string; at: Vec2 };
export type GraphicVector = {
  label?: string;
  from: Vec2;
  to: Vec2;
  color?: string;
  dashed?: boolean;
};

export type VectorPlotGraphic = {
  kind: "vector-plot";
  xRange: Vec2;
  yRange: Vec2;
  gridStep?: number;
  points?: GraphicPoint[];
  vectors?: GraphicVector[];
};

export type RightTriangleLabels = {
  A?: string;
  B?: string;
  C?: string;
  a?: string;
  b?: string;
  c?: string;
  h?: string;
  m?: string;
  n?: string;
};

export type RightTriangleGraphic = {
  kind: "right-triangle";
  b: number;
  c: number;
  labels?: RightTriangleLabels;
  showAltitude?: boolean;
  highlight?: Array<"a" | "b" | "c" | "h" | "m" | "n">;
};

export type AppliedTriangleGraphic = {
  kind: "applied-triangle";
  angleDeg: number;
  labels?: {
    opposite?: string;
    adjacent?: string;
    hypotenuse?: string;
    angle?: string;
  };
  vertexLabels?: {
    rightAngle?: string;
    acuteAngle?: string;
    top?: string;
  };
  highlight?: Array<"opposite" | "adjacent" | "hypotenuse">;
};

export type ShapePiece =
  | { type: "polygon"; points: Vec2[]; dashed?: boolean; filled?: boolean; highlight?: boolean }
  | { type: "circle"; center: Vec2; r: number; dashed?: boolean; filled?: boolean; highlight?: boolean }
  | {
      type: "arc";
      center: Vec2;
      r: number;
      fromDeg: number;
      toDeg: number;
      closed?: boolean;
      dashed?: boolean;
      filled?: boolean;
      highlight?: boolean;
    }
  | { type: "line"; from: Vec2; to: Vec2; dashed?: boolean; highlight?: boolean };

export type ShapeLabel = {
  at: Vec2;
  text: string;
  anchor?: "start" | "middle" | "end";
  color?: "default" | "highlight" | "muted";
  bold?: boolean;
};

export type ShapePlotGraphic = {
  kind: "shape-plot";
  viewBox: [number, number, number, number];
  shapes: ShapePiece[];
  labels?: ShapeLabel[];
};

export type Graphic =
  | VectorPlotGraphic
  | RightTriangleGraphic
  | AppliedTriangleGraphic
  | ShapePlotGraphic;

export type Step =
  | { kind: "text"; text: string }
  | { kind: "math"; tex: string }
  | { kind: "graphic"; graphic: Graphic };

export type Question = {
  id: string;
  statement: string;
  graphic?: Graphic;
  options: string[];
  correct: number;
  resolution: Step[];
};

export type Topic = {
  id: string;
  name: string;
  description?: string;
  questions: Question[];
};

export type TopicIndexEntry = {
  id: string;
  name: string;
  file: string;
};

export type TopicIndex = { topics: TopicIndexEntry[] };
