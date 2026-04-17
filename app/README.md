# Mates 4t ESO — Pràctica

Aplicació SPA de suport a l'estudi per practicar exercicis de matemàtiques de 4t d'ESO.
La interfície és en **català**; les *specs* internes, a `../specs/`, estan en castellà.

> Per al desplegament amb Docker, consulta el [`README.md`](../README.md) de l'arrel.

## Posar-la en marxa (desenvolupament)

```bash
cd app
npm install
npm run dev          # Vite (client) + Express (API) en paral·lel
```

Vite fa proxy de `/api` a `http://localhost:3001`.

## Producció sense Docker

```bash
cd app
npm install
npm run build        # tsc --noEmit + vite build → dist/
npm start            # node server/index.mjs (serveix API + dist/ al port 3001)
```

## Afegir preguntes / temes

1. Crea un nou JSON a `public/topics/` amb l'estructura de `Topic` (vegeu `src/types.ts`).
   Cada tema ha de tenir **exactament 25 preguntes** amb **4 opcions** cadascuna.
2. Afegeix-lo a `public/topics/index.json`.
3. No cal tocar codi.

Els generadors Python a `../scripts/` creen els JSON automàticament amb
validacions (25 preguntes, 4 opcions úniques, índex correcte dins de rang).

## Estructura

- `server/` — API REST (Express) i persistència del progrés.
  - `server/index.mjs` — servidor Express (API + estàtic).
  - `server/data/progress.json` — fitxer de progrés (escritura atòmica).
- `public/topics/` — fitxers JSON de temes (servits estàticament).
- `src/components/` — UI: selector, pregunta, opcions, resolució i gràfics
  (`VectorPlot`, `RightTrianglePlot`, `AppliedTrianglePlot`, `ShapePlot`,
  encaminats per `GraphicView`).
- `src/data/` — càrrega de temes (`loadTopics.ts`) i client del progrés
  (`progress.ts`: caché en memòria + actualització optimista contra l'API).
- `src/types.ts` — tipus de dades (`Topic`, `Question`, `Graphic`, `Step`…).
- `src/i18n.ts` — totes les cadenes de la UI en català.

## Progrés

Es guarda al **servidor** (`server/data/progress.json`), de manera que és
accessible des de qualsevol navegador que apunti al mateix backend. No hi ha
comptes ni autenticació: el progrés és global i compartit (un únic alumne
objectiu).

Quan es completen tots els exercicis d'un tema, es mostra un missatge amb
l'opció **"Tornar a començar"** (amb confirmació). També hi ha un botó de
*Reiniciar* al selector. A la *home* es mostren, per cada tema, els exercicis
fets i quants han estat correctes (✓) o errats (✗).
