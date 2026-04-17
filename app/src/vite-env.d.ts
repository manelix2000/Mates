declare module "react-katex" {
  import { ComponentType } from "react";
  type Props = {
    math: string;
    renderError?: (error: Error) => JSX.Element;
    errorColor?: string;
  };
  export const InlineMath: ComponentType<Props>;
  export const BlockMath: ComponentType<Props>;
}

interface ImportMetaEnv {
  readonly BASE_URL: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
