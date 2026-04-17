import type { Graphic } from "../types";
import { VectorPlot } from "./VectorPlot";
import { RightTrianglePlot } from "./RightTrianglePlot";
import { AppliedTrianglePlot } from "./AppliedTrianglePlot";
import { ShapePlot } from "./ShapePlot";

type Props = {
  graphic: Graphic;
  size?: number;
};

export function GraphicView({ graphic, size }: Props) {
  if (graphic.kind === "vector-plot") {
    return <VectorPlot graphic={graphic} size={size} />;
  }
  if (graphic.kind === "right-triangle") {
    return <RightTrianglePlot graphic={graphic} size={size} />;
  }
  if (graphic.kind === "applied-triangle") {
    return <AppliedTrianglePlot graphic={graphic} size={size} />;
  }
  if (graphic.kind === "shape-plot") {
    return <ShapePlot graphic={graphic} size={size} />;
  }
  return null;
}
