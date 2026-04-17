# Mates 4t ESO — Pràctica

Aplicació SPA de suport a l'estudi per practicar exercicis de matemàtiques de 4t d'ESO.
La interfície és en **català**; les *specs* internes, a `../specs/`, estan en castellà.

## Posar-la en marxa

```bash
cd app
npm install
npm run dev        # desenvolupament
npm run build      # build estàtic a dist/
npm run preview    # servir el build
```

## Afegir preguntes / temes

1. Crea un nou JSON a `public/topics/` amb l'estructura de `Topic` (vegeu `src/types.ts`).
2. Afegeix-lo a `public/topics/index.json`.
3. No cal tocar codi.

## Estructura

- `public/topics/` — fitxers JSON de temes (servits estàticament).
- `src/components/` — UI (selector, pregunta, opcions, resolució, plot vectorial).
- `src/data/` — càrrega de temes i persistència de progrés (`localStorage`).
- `src/types.ts` — tipus de dades (`Topic`, `Question`, `Graphic`, `Step`…).
- `src/i18n.ts` — totes les cadenes de la UI en català.

## Progrés

Es guarda al navegador (`localStorage`, clau `mates1.progress.<topicId>`).
Quan es completen tots els exercicis d'un tema, es mostra un missatge amb l'opció
**"Tornar a començar"** (amb confirmació). També hi ha un botó de *Reiniciar* al selector.
