# FlyTrack Backend

Backend minimo viable para AeroPuerto Smart. Implementa solo las capacidades mencionadas para FlyTrack: consultar itinerarios, recibir notificaciones sobre cambios de vuelo, conocer la puerta de embarque y reportar inconvenientes con equipaje.

## Ejecucion local

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Swagger queda disponible en:

```text
http://localhost:8000/docs
```

## Endpoints

- `GET /itinerarios`
- `GET /itinerarios/{numero_vuelo}`
- `GET /puertas-embarque/{numero_vuelo}`
- `GET /notificaciones?numero_vuelo=FT204`
- `POST /equipaje/reportes`

## Pruebas

```bash
pytest
```

## Contenedores

```bash
docker compose up --build
```

## Monitoreo

El stack incluye Prometheus y Grafana para monitoreo en tiempo real:

- **Health check:** `GET /health` — verifica el estado del servicio
- **Metricas:** `GET /metrics` — metricas en formato Prometheus
- **Prometheus:** `http://localhost:9090` — recoleccion de metricas
- **Grafana:** `http://localhost:3000` — dashboards visuales (admin / flytrack2026)

Metricas expuestas:
- `flytrack_requests_total` — contador de peticiones por metodo, endpoint y status
- `flytrack_request_duration_seconds` — histograma de latencia

## Pipeline DevOps

El flujo en `.github/workflows/ci-cd.yml` cubre las etapas solicitadas:

1. **Build & Test:** instalacion de dependencias, pruebas automatizadas con pytest
2. **Quality:** analisis de calidad con Ruff
3. **Docker:** build y push de imagen a GitHub Container Registry (GHCR)
4. **Staging:** despliegue automatico a EC2 via SSH + validacion con health check
5. **Produccion:** despliegue a produccion tras staging exitoso

## Despliegue

Consultar la guia completa en [`docs/DEPLOY_GUIDE.md`](docs/DEPLOY_GUIDE.md).

## Diagnostico y decisiones

El documento describe problemas de despliegues lentos, fallos inesperados, falta de control de versiones, ausencia de pruebas automatizadas, infraestructura manual y comunicacion limitada. Esta implementacion responde con control de versiones, pruebas unitarias, contenedor Docker, Docker Compose, pipeline CI/CD con despliegue real a AWS EC2, y monitoreo con Prometheus/Grafana para reducir errores manuales, hacer repetible la entrega del backend y detectar problemas en tiempo real.
