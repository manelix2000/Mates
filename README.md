# Mates 4t ESO — Desplegament

Aplicació SPA de pràctica de matemàtiques de 4t d'ESO (React + Vite + Express)
empaquetada en un únic contenidor Docker. El servidor Express serveix tant
l'API REST (`/api/*`) com el build estàtic del SPA.

> Per al codi font, generadors de preguntes i guia de desenvolupament,
> consulta [`app/README.md`](./app/README.md).

---

## Requisits

- Docker Engine **≥ 24** amb el plugin **Compose v2** (`docker compose ...`).
- Port lliure al host (per defecte `3001`, configurable).

Comprovació ràpida:

```bash
docker --version
docker compose version
```

---

## Desplegament ràpid

Des de l'arrel del repositori:

```bash
docker compose up -d --build
```

L'aplicació queda disponible a `http://localhost:3001`.

Per veure els logs:

```bash
docker compose logs -f mates1
```

Per aturar-la:

```bash
docker compose down
```

---

## Configuració

### Port

Es pot canviar amb la variable `PORT` (mapeig `host:contenidor`):

```bash
PORT=8080 docker compose up -d
```

O fixant-ho en un fitxer `.env` al costat de `docker-compose.yml`:

```env
PORT=8080
```

### Persistència del progrés

El servidor desa el progrés (encerts/errors per pregunta) a
`/app/server/data/progress.json` dins del contenidor. Aquest path es persisteix
mitjançant un **volum nomenat** (`mates1-data`) declarat al `docker-compose.yml`,
de manera que el progrés sobreviu a reconstruccions i actualitzacions.

Inspecció del volum:

```bash
docker volume inspect mates1_mates1-data
```

Backup del progrés a un tarball local:

```bash
docker run --rm \
  -v mates1_mates1-data:/data \
  -v "$PWD":/backup \
  alpine tar czf /backup/progress-backup.tar.gz -C /data .
```

Restaurar des d'un backup:

```bash
docker run --rm \
  -v mates1_mates1-data:/data \
  -v "$PWD":/backup \
  alpine sh -c "cd /data && tar xzf /backup/progress-backup.tar.gz"
```

> ⚠️ Si vols **esborrar el progrés**, fes `docker compose down -v` (la `-v`
> elimina també el volum). Sense la `-v` les dades es conserven.

---

## Actualitzacions

Quan canviï el codi, els temes (`app/public/topics/*.json`) o el `Dockerfile`:

```bash
docker compose up -d --build
```

Compose reconstruirà la imatge i recrearà el contenidor; el volum de dades es
manté intacte.

---

## Endpoints exposats

Una vegada en marxa, el contenidor exposa:

| Mètode    | Ruta                              | Descripció                                   |
| --------- | --------------------------------- | -------------------------------------------- |
| `GET`     | `/`                               | SPA (React)                                  |
| `GET`     | `/api/progress`                   | Tot el progrés (tots els temes)              |
| `GET`     | `/api/progress/:topicId`          | Progrés d'un tema concret                    |
| `POST`    | `/api/progress/:topicId/answer`   | Registra una resposta `{ questionId, correct }` |
| `DELETE`  | `/api/progress/:topicId`          | Reinicia el progrés d'un tema                |

El healthcheck del contenidor consulta `GET /api/progress`.

---

## Reverse proxy (opcional)

Si vols servir-la darrere d'un reverse proxy (nginx, Caddy, Traefik), exposa
internament el port `3001` i deixa que el proxy gestioni TLS i el domini
públic. Exemple mínim amb **Caddy**:

```caddy
mates.example.com {
    reverse_proxy localhost:3001
}
```

Si fas servir Traefik amb labels, el `docker-compose.yml` és fàcilment
ampliable; demana-ho i s'afegeixen.

---

## Resolució de problemes

**El port 3001 ja està ocupat al host**
Canvia el mapeig amb `PORT=NOUPORT docker compose up -d`.

**El progrés no es persisteix**
Verifica que el volum existeix i està montat:
```bash
docker compose ps
docker volume ls | grep mates1
docker exec -it mates1 ls -la /app/server/data
```

**El healthcheck queda en `unhealthy`**
Mira els logs (`docker compose logs mates1`) i comprova que `/api/progress`
respon dins del contenidor:
```bash
docker exec -it mates1 wget -qO- http://127.0.0.1:3001/api/progress
```

**Reconstrucció neta (si la cau de Docker fa coses estranyes)**
```bash
docker compose build --no-cache
docker compose up -d
```
