# syntax=docker/dockerfile:1.7

# ---------- Etapa 1: build del SPA ----------
FROM node:20-alpine AS builder

WORKDIR /app

# Instalación reproducible con package-lock
COPY package.json package-lock.json ./
RUN npm ci

# Copiamos sólo lo necesario para compilar el cliente
COPY tsconfig.json vite.config.ts tailwind.config.js postcss.config.js index.html ./
COPY src ./src
COPY public ./public

RUN npm run build

# ---------- Etapa 2: runtime ----------
FROM node:20-alpine AS runtime

ENV NODE_ENV=production \
    PORT=3001

WORKDIR /app

# Sólo dependencias de producción (express)
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Servidor + assets construidos
COPY server ./server
COPY --from=builder /app/dist ./dist

# Directorio persistente para progress.json (montar como volumen)
RUN mkdir -p /app/server/data \
    && chown -R node:node /app

USER node

EXPOSE 3001

# Healthcheck contra el endpoint de progreso
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3001/api/progress > /dev/null || exit 1

CMD ["node", "server/index.mjs"]
