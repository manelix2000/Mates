# Roadmap

Estado actual del proyecto. Las casillas marcadas reflejan trabajo completado.
No se incluyen estimaciones temporales.

## Fase 0 — Andamiaje
- [x] Proyecto Vite + React + TypeScript inicializado.
- [x] Tailwind CSS configurado.
- [x] Estructura de carpetas conforme a `tech-stack.md`.
- [x] Tipos en `src/types.ts` cubriendo `Topic`, `Question`, `Step` y los 4
      tipos de `Graphic`.
- [ ] ESLint + Prettier explícitos (pendiente; actualmente solo `tsc --noEmit`).

## Fase 1 — Carga de temas desde JSON
- [x] `loadTopics.ts` lee `public/topics/index.json` y los JSON individuales.
- [x] `TopicSelector` con la lista de temas + estadísticas (fets / ✓ / ✗).
- [x] Tolerancia mínima a JSON inválido (estructura por defecto vacía).

## Fase 2 — Motor de preguntas
- [x] `QuestionView`: enunciado + gráfico (si hay) + opciones.
- [x] `OptionList`: 4 botones con selección única.
- [x] Botón **"Comprova"**: bloquea selección, marca correcta/incorrecta, muestra
      la resolución paso a paso.
- [x] Botón **"Següent"**: avanza a la siguiente pregunta pendiente del tema.
- [x] Orden aleatorio entre las preguntas pendientes.
- [x] UI 100 % en catalán (fichero `i18n.ts`).

## Fase 2b — Persistencia y reinicio (servidor, no localStorage)
- [x] Servidor Express con persistencia en `server/data/progress.json`.
- [x] API REST: `GET /api/progress`, `GET /api/progress/:topicId`,
      `POST /api/progress/:topicId/answer`, `DELETE /api/progress/:topicId`.
- [x] Escritura atómica (rename desde `.tmp`) y lock serie en memoria.
- [x] Validación regex de `topicId` y `questionId`.
- [x] Cliente `progress.ts` con caché en memoria, deduplicación de inflight y
      actualización optimista (la UI no espera al servidor).
- [x] `TopicCompleted` con botón **"Tornar a començar"** (con confirmación).
- [x] Reset manual desde el selector (con confirmación).
- [x] Persistencia por ID (no por índice): tolera cambios en los JSON.
- [x] Estadísticas por tema en la home: fets, correctos, errados.

## Fase 3 — Renderizado gráfico
- [x] `VectorPlot`: ejes, cuadrícula, puntos con etiqueta, vectores con flecha.
- [x] `RightTrianglePlot`: triángulo rectángulo con altura y proyecciones.
- [x] `AppliedTrianglePlot`: triángulo con ángulo agudo etiquetado y vértices
      contextuales (terra/extrem/observador…).
- [x] `ShapePlot`: lienzo genérico (polygon/circle/arc/line + labels libres) con
      auto-fit del viewBox y escalado proporcional de fuente y trazos.
- [x] `GraphicView` como router único de tipos de gráfico.
- [x] Soporte de gráficos auxiliares dentro de los pasos de resolución.
- [x] Responsive (los SVG escalan al ancho del contenedor).

## Fase 4 — Resoluciones paso a paso
- [x] `Resolution` que renderiza una lista de `Step`.
- [x] Soporte de `text`, `math` (KaTeX) y `graphic`.
- [x] Convención: cada tema con incógnitas geométricas cierra la resolución con
      un gráfico final con todos los valores resueltos.

## Fase 5 — Contenido (6 temas publicados, 25 preguntas × 4 opciones)
- [x] `vectors-graphic.json` — construcció gràfica (suma i resta).
- [x] `vectors-compute.json` — suma i resta (càlcul).
- [x] `vectors-endpoints.json` — coordenades d'un extrem (A o B).
- [x] `right-triangles-theorems.json` — Pitàgores + teorema de l'altura
      (cada pregunta pide más de una magnitud; **sin teorema del catete**).
- [x] `applied-right-triangles.json` — problemas de trigonometría aplicada
      (palos, escaleras, rampas, ángulos de elevación/depresión, etc.) usando
      `sin`/`cos` y Pitàgores en lugar de `tan`/`arctan`.
- [x] `shapes-perimeter-area.json` — perímetros y áreas de figuras básicas
      (cuadrado, rectángulo, triángulo rectángulo, trapecio, círculo) y
      **figuras compuestas** por dos figuras básicas.
- [x] Generadores Python en `scripts/` para regenerar cada tema con
      validaciones (25 preguntas, 4 opciones únicas, índice correcto).

## Fase 6 — Despliegue
- [x] `npm run build` produce `dist/` estático y `npm start` lanza el servidor
      Express que sirve API + estático en el mismo puerto.
- [x] **Dockerización**: `Dockerfile` multi-stage en `app/` y
      `docker-compose.yml` en la raíz con volumen nomenado para persistir
      `progress.json` entre redeploys.
- [x] `README.md` de la raíz con la guía de despliegue Docker (build, logs,
      backup/restore del progreso, healthcheck, reverse proxy opcional).
- [ ] Despliegue real en un servidor accesible desde fuera de la red local
      (pendiente; opcional).

## Mejoras de pulido aplicadas
- [x] Mensajes de feedback claros (✓ / ✗ con colores suaves).
- [x] Estados de carga y error con mensaje en catalán.
- [x] Responsive básico para móvil/tablet.

## Futuro (sin compromiso)
- Nuevos temas: sistemas de ecuaciones, probabilidad, funciones afines,
  estadística descriptiva, semejanza de triángulos, polinomios.
- Reverse proxy con TLS y dominio público (Caddy o Traefik) si se decide
  exponer la app fuera de la red local.
- Marcado de preguntas favoritas / "repasar".
- Modo "serie de N preguntas" con resumen final.
- Generación procedural de variantes a partir de un mismo enunciado plantilla.
- Refactor opcional: unificar `RightTrianglePlot` y `AppliedTrianglePlot` como
  casos particulares de `ShapePlot` para reducir componentes.
- Editor visual de preguntas (muy bajo en prioridad).
