# Guía de Despliegue - FlyTrack

## Arquitectura del Pipeline

```
Push a main → Build & Test → Quality (Ruff) → Docker Build & Push (GHCR) → Deploy Staging (EC2) → Deploy Producción (EC2)
```

## 1. Configurar Secrets en GitHub

Configurar estos secrets en **AMBOS repositorios** (Backend y Frontend):

Ve a **Settings → Secrets and variables → Actions** de cada repositorio y crea:

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `EC2_HOST` | IP pública o DNS de tu instancia EC2 | `54.123.45.67` |
| `EC2_USER` | Usuario SSH de la instancia | `ubuntu` o `ec2-user` |
| `EC2_SSH_KEY` | Llave privada SSH (contenido completo del `.pem`) | `-----BEGIN RSA PRIVATE KEY-----...` |

**Solo en el repo Frontend** (Front.FlyTrack), agregar además:

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `VITE_API_URL` | URL pública del backend en EC2 | `http://54.123.45.67:8000` |

> **Nota:** `GITHUB_TOKEN` se genera automáticamente por GitHub Actions, no es necesario configurarlo manualmente.

## 2. Configurar Environments en GitHub

En **ambos repositorios**, ve a **Settings → Environments** y crea dos environments:

- **staging** — se despliega automáticamente tras el build exitoso
- **production** — puedes agregar protección con revisores si deseas aprobación manual antes del deploy

## 3. Preparar la VM EC2

Conéctate por SSH a tu instancia y ejecuta:

```bash
# Crear las carpetas de proyecto
mkdir -p ~/flytrack ~/flytrack-staging

# Clonar el repositorio (para obtener docker-compose y configs)
cd ~/flytrack
git clone https://github.com/SebasGalle07/FlyTrack.git .

# Copiar lo mismo para staging
cp -r ~/flytrack/* ~/flytrack-staging/

# Verificar que Docker funciona
docker --version
docker compose version
```

### Puertos necesarios en el Security Group de AWS

Abre estos puertos en el Security Group de tu instancia EC2:

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 22 | SSH | Acceso remoto |
| 5173 | FlyTrack Frontend | Interfaz web |
| 8000 | FlyTrack API | API backend |
| 9090 | Prometheus | Métricas |
| 3000 | Grafana | Dashboard de monitoreo |

## 4. Primer despliegue manual (opcional)

Para verificar que todo funciona antes de usar el pipeline:

```bash
cd ~/flytrack

# Login al registry
echo "TU_GITHUB_TOKEN" | docker login ghcr.io -u TU_USUARIO --password-stdin

# Levantar todo el stack
docker compose up -d --build

# Verificar
curl http://localhost:8000/health
curl http://localhost:9090/-/healthy
```

## 5. Acceder al monitoreo

Una vez desplegado:

- **Frontend:** `http://<IP_EC2>:5173` — Interfaz web de FlyTrack
- **API:** `http://<IP_EC2>:8000/docs` — Swagger de la API
- **Health Check:** `http://<IP_EC2>:8000/health`
- **Prometheus:** `http://<IP_EC2>:9090` — Explorador de métricas
- **Grafana:** `http://<IP_EC2>:3000` — Dashboard visual
  - Usuario: `admin`
  - Contraseña: `flytrack2026`

## 6. Métricas disponibles

La API expone estas métricas en `/metrics` (formato Prometheus):

| Métrica | Tipo | Descripción |
|---------|------|-------------|
| `flytrack_requests_total` | Counter | Total de peticiones HTTP (por método, endpoint, status) |
| `flytrack_request_duration_seconds` | Histogram | Latencia de peticiones (por método, endpoint) |

## 7. Flujo de trabajo diario

1. Los desarrolladores hacen push a `main`
2. GitHub Actions ejecuta tests y análisis de calidad
3. Si pasan, construye y publica la imagen Docker en GHCR
4. Despliega automáticamente en staging
5. Si staging es exitoso, despliega en producción
6. Monitorea en Grafana que todo esté funcionando correctamente
