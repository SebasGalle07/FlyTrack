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

## Pipeline DevOps

El flujo en `.github/workflows/ci-cd.yml` cubre las etapas solicitadas: compilacion/preparacion del entorno, pruebas automatizadas, analisis de calidad con Ruff, empaquetado con Docker y despliegue controlado a `staging` y `production`.

## Diagnostico y decisiones

El documento describe problemas de despliegues lentos, fallos inesperados, falta de control de versiones, ausencia de pruebas automatizadas, infraestructura manual y comunicacion limitada. Esta implementacion responde con control de versiones, pruebas unitarias, contenedor Docker, Docker Compose y pipeline CI/CD basico para reducir errores manuales y hacer repetible la entrega del backend.
