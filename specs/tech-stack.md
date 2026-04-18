# Stack tecnológico

## Tipo de aplicación
Aplicación web full-stack mínima:

- **Cliente:** SPA (React + TypeScript) que se construye estáticamente con Vite.
- **Servidor:** API REST minimalista en Node + Express que también sirve el build
  estático del cliente (un único proceso para SPA + API).

No hay base de datos: la persistencia se hace sobre un único fichero JSON con
escritura atómica.

## Cliente
- **Framework:** React 18 + TypeScript (modo estricto).
- **Bundler / dev server:** Vite 5.
- **Estilos:** Tailwind CSS 3.
- **Routing:** ninguno (una sola vista con estados internos).
- **Renderizado matemático:** KaTeX (`react-katex`) para fracciones, raíces, vectores, etc.
- **Renderizado gráfico:** SVG nativo, declarativo desde JSON.

## Servidor
- **Runtime:** Node 20.
- **Framework HTTP:** Express 4.
- **Persistencia:** un único fichero `app/server/data/progress.json`.
  - Escritura atómica: se escribe a `progress.json.tmp` y se hace `rename`.
  - Lock serie en memoria (`writeChain`) para evitar carreras entre peticiones
    concurrentes.
  - Validación estricta de `topicId` y `questionId` por regex
    (`/^[a-z0-9][a-z0-9-]{0,63}$/i` y `/^[a-z0-9_-]{1,64}$/i`).
- **Servicio del SPA:** si existe `app/dist/`, Express lo monta como estático
  y devuelve `index.html` para cualquier ruta no-API (fallback SPA).

### API REST
| Método  | Ruta                              | Descripción                           |
| ------- | --------------------------------- | ------------------------------------- |
| `GET`   | `/api/progress`                   | Estado completo (todos los temas).    |
| `GET`   | `/api/progress/:topicId`          | Progreso de un tema concreto.         |
| `POST`  | `/api/progress/:topicId/answer`   | Body `{questionId, correct}`.         |
| `DELETE`| `/api/progress/:topicId`          | Resetea el progreso del tema.         |

Estructura de cada tema en el JSON:
```ts
type TopicProgress = {
  version: 1;
  answered: { [questionId: string]: { correct: boolean; at: string /* ISO */ } };
};
```

### Cliente de progreso
- Módulo `src/data/progress.ts`:
  - Caché en memoria por tema + deduplicación de peticiones inflight.
  - `getProgress(topicId)`, `markAnswered(topicId, questionId, correct)`,
    `resetTopic(topicId)`, `getAllProgress()`, `pendingQuestions(topic, progress)`.
  - **Actualización optimista** en `markAnswered`: la UI no espera al servidor.
    Si la red falla, se registra un `console.warn` y la sesión sigue funcionando
    con el caché en memoria.
- Pendientes calculados **por diferencia de IDs** (no por índice), de modo que
  añadir o eliminar preguntas en el JSON no rompe el progreso existente.

## Idioma de la UI
- Toda la interfaz y los contenidos servidos desde JSON están en **catalán**.
- Las specs internas siguen en **castellano**.
- Cadenas centralizadas en `src/i18n.ts`.

## Carga de temas
- Cada tema es un fichero JSON en `app/public/topics/` (servido estático).
- `app/public/topics/index.json` lista los temas disponibles.
- La app hace `fetch()` al abrir el selector y al elegir un tema.
- Añadir un tema = añadir su JSON + una entrada en el índice. **Sin tocar código.**

## Esquema de datos
```ts
type Topic = {
  id: string;
  name: string;
  description?: string;
  questions: Question[];      // siempre 25
};

type Question = {
  id: string;
  statement: string;          // texto, puede incluir $...$ para KaTeX
  graphic?: Graphic;          // opcional, descripción declarativa del SVG
  options: string[];          // exactamente 4
  correct: number;            // índice 0..3
  resolution: Step[];         // pasos de la explicación
};

type Step =
  | { kind: "text";    text: string }
  | { kind: "math";    tex:  string }
  | { kind: "graphic"; graphic: Graphic };

type Graphic =
  | VectorPlotGraphic
  | RightTriangleGraphic
  | AppliedTriangleGraphic
  | ShapePlotGraphic;
```

### Tipos de gráfico

#### `vector-plot`
Plano cartesiano con cuadrícula, puntos y vectores con flecha.
```ts
type VectorPlotGraphic = {
  kind: "vector-plot";
  xRange: [number, number];
  yRange: [number, number];
  gridStep?: number;
  points?:  { label: string; at: [number, number] }[];
  vectors?: {
    label?: string;
    from:  [number, number];
    to:    [number, number];
    color?: string;
    dashed?: boolean;
  }[];
};
```

#### `right-triangle`
Triángulo rectángulo con catetos `b`, `c`, posibilidad de dibujar la altura
sobre la hipotenusa y proyecciones `m`, `n`. Usado en el tema de teoremas.
```ts
type RightTriangleGraphic = {
  kind: "right-triangle";
  b: number;                  // cateto horizontal
  c: number;                  // cateto vertical
  labels?: {
    A?: string; B?: string; C?: string;       // vértices
    a?: string; b?: string; c?: string;       // lados
    h?: string; m?: string; n?: string;       // altura y proyecciones
  };
  showAltitude?: boolean;
  highlight?: Array<"a" | "b" | "c" | "h" | "m" | "n">;
};
```

#### `applied-triangle`
Triángulo rectángulo aplicado con un ángulo agudo `α`. Pensado para problemas
reales (palos, escaleras, rampas, ángulos de elevación/depresión).
```ts
type AppliedTriangleGraphic = {
  kind: "applied-triangle";
  angleDeg: number;
  labels?: {
    opposite?: string;
    adjacent?: string;
    hypotenuse?: string;
    angle?: string;
  };
  vertexLabels?: {
    rightAngle?: string;      // vértice del ángulo recto (suelo)
    acuteAngle?: string;      // vértice del ángulo α (observador)
    top?: string;             // vértice superior (extremo)
  };
  highlight?: Array<"opposite" | "adjacent" | "hypotenuse">;
};
```

#### `shape-plot`
Lienzo genérico con `viewBox` lógico y una lista de primitivas más etiquetas
libres en posiciones absolutas. Permite cualquier figura plana y figuras
**compuestas** (rectángulo + semicírculo, cuadrado + triángulo, L de dos
rectángulos, placa con agujero…).
```ts
type ShapePlotGraphic = {
  kind: "shape-plot";
  viewBox: [number, number, number, number];   // fallback; se auto-ajusta
  shapes: ShapePiece[];
  labels?: ShapeLabel[];
};

type ShapePiece =
  | { type: "polygon"; points: [number, number][];
      dashed?: boolean; filled?: boolean; highlight?: boolean }
  | { type: "circle";  center: [number, number]; r: number;
      dashed?: boolean; filled?: boolean; highlight?: boolean }
  | { type: "arc";     center: [number, number]; r: number;
      fromDeg: number; toDeg: number; closed?: boolean;
      dashed?: boolean; filled?: boolean; highlight?: boolean }
  | { type: "line";    from: [number, number]; to: [number, number];
      dashed?: boolean; highlight?: boolean };

type ShapeLabel = {
  at: [number, number];
  text: string;
  anchor?: "start" | "middle" | "end";
  color?: "default" | "highlight" | "muted";
  bold?: boolean;
};
```
El componente `ShapePlot` calcula el bounding box real de las primitivas y
aplica un padding del ~18 % para que la figura ocupe el máximo del SVG. El
tamaño de fuente y el grosor de línea se escalan en unidades del viewBox para
mantener proporciones independientes del zoom.

## Estructura de carpetas
```
/
├─ README.md                  (despliegue Docker)
├─ docker-compose.yml
├─ specs/                     (este directorio)
│  ├─ mission.md
│  ├─ tech-stack.md
│  └─ roadmap.md
├─ scripts/                   (generadores Python de temas)
│  ├─ gen_vectors_*.py
│  ├─ gen_right_triangles_theorems.py
│  ├─ gen_applied_right_triangles.py
│  └─ gen_shapes_perimeter_area.py
└─ app/
   ├─ Dockerfile
   ├─ .dockerignore
   ├─ package.json
   ├─ vite.config.ts          (proxy /api → :3001 en dev)
   ├─ tailwind.config.js
   ├─ tsconfig.json
   ├─ index.html
   ├─ public/
   │  └─ topics/
   │     ├─ index.json
   │     ├─ vectors-graphic.json
   │     ├─ vectors-compute.json
   │     ├─ vectors-endpoints.json
   │     ├─ right-triangles-theorems.json
   │     ├─ applied-right-triangles.json
   │     ├─ shapes-perimeter-area.json
   │     └─ volumes.json
   ├─ server/
   │  ├─ index.mjs            (Express: API + estático)
   │  └─ data/
   │     └─ progress.json     (persistido; volumen Docker)
   └─ src/
      ├─ main.tsx
      ├─ App.tsx
      ├─ types.ts
      ├─ i18n.ts
      ├─ data/
      │  ├─ loadTopics.ts
      │  └─ progress.ts       (cliente del API)
      ├─ components/
      │  ├─ TopicSelector.tsx
      │  ├─ TopicCompleted.tsx
      │  ├─ QuestionView.tsx
      │  ├─ OptionList.tsx
      │  ├─ Resolution.tsx
      │  ├─ RichText.tsx
      │  ├─ GraphicView.tsx           (router de tipos de gráfico)
      │  ├─ VectorPlot.tsx
      │  ├─ RightTrianglePlot.tsx
      │  ├─ AppliedTrianglePlot.tsx
      │  └─ ShapePlot.tsx
      └─ styles/index.css
```

## Calidad / convenciones
- TypeScript en modo estricto; `tsc --noEmit` forma parte de `npm run build`.
- Componentes funcionales con hooks; sin estado global complejo.
- Sin tests automatizados (la app es personal y los generadores Python validan
  por su cuenta: 25 preguntas, 4 opciones únicas, índice correcto en rango).
- Linters/formatters: confianza en convenciones del editor (no se ha añadido
  ESLint/Prettier explícito).

## Despliegue

### Desarrollo local
```bash
cd app
npm install
npm run dev          # vite + servidor en paralelo (concurrently)
```
Vite hace proxy de `/api` a `http://localhost:3001`.

### Producción local sin Docker
```bash
cd app
npm install
npm run build        # tsc --noEmit + vite build → dist/
npm start            # node server/index.mjs
```
Express sirve `dist/` y la API en el mismo puerto (3001).

### Producción con Docker
Desde la raíz del repositorio:
```bash
docker compose up -d --build
```
El `Dockerfile` es multi-stage:
1. **builder** (`node:20-alpine`): `npm ci` + `npm run build`.
2. **runtime** (`node:20-alpine`): `npm ci --omit=dev` + copia `server/` y
   `dist/` del builder. Corre como user `node`. Healthcheck contra
   `/api/progress`.

`docker-compose.yml` declara un volumen nomenado `mates1-data` montado en
`/app/server/data` para que el progreso sobreviva a redeploys.

Detalles completos en el `README.md` de la raíz.
