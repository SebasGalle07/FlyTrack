import os
import time
from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.requests import Request
from starlette.responses import Response

from app.models import (
    ErrorRespuesta,
    Itinerario,
    Notificacion,
    PuertaEmbarque,
    ReporteEquipaje,
    ReporteEquipajeEntrada,
)
from app.repository import (
    buscar_itinerario,
    buscar_puerta,
    itinerarios,
    listar_notificaciones,
    registrar_reporte_equipaje,
)

from fastapi.middleware.cors import CORSMiddleware

REQUEST_COUNT = Counter(
    "flytrack_requests_total",
    "Total de peticiones HTTP",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "flytrack_request_duration_seconds",
    "Latencia de peticiones HTTP",
    ["method", "endpoint"],
)

app = FastAPI(
    title="FlyTrack API",
    description="Backend de AeroPuerto Smart para itinerarios, notificaciones, puertas de embarque y reportes de equipaje.",
    version="1.0.0",
)

_extra_origins = os.getenv("CORS_ORIGINS", "")
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
] + [o.strip() for o in _extra_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    endpoint = request.url.path
    REQUEST_COUNT.labels(
        method=request.method, endpoint=endpoint, status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)
    return response


@app.get("/health", summary="Health check", tags=["ops"])
def health_check():
    return {
        "status": "healthy",
        "service": "flytrack-api",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


@app.get("/metrics", summary="Prometheus metrics", tags=["ops"], include_in_schema=False)
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get(
    "/itinerarios",
    response_model=list[Itinerario],
    summary="Consultar itinerarios",
)
def consultar_itinerarios() -> list[Itinerario]:
    return itinerarios


@app.get(
    "/itinerarios/{numero_vuelo}",
    response_model=Itinerario,
    responses={404: {"model": ErrorRespuesta}},
    summary="Consultar itinerario por vuelo",
)
def consultar_itinerario(numero_vuelo: str) -> Itinerario:
    itinerario = buscar_itinerario(numero_vuelo)
    if itinerario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vuelo no encontrado")
    return itinerario


@app.get(
    "/puertas-embarque/{numero_vuelo}",
    response_model=PuertaEmbarque,
    responses={404: {"model": ErrorRespuesta}},
    summary="Conocer puerta de embarque",
)
def consultar_puerta_embarque(numero_vuelo: str) -> PuertaEmbarque:
    puerta = buscar_puerta(numero_vuelo)
    if puerta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puerta no encontrada")
    return puerta


@app.get(
    "/notificaciones",
    response_model=list[Notificacion],
    summary="Recibir notificaciones sobre cambios de vuelo",
)
def consultar_notificaciones(
    numero_vuelo: Annotated[
        str | None,
        Query(description="Numero de vuelo para filtrar notificaciones"),
    ] = None,
) -> list[Notificacion]:
    return listar_notificaciones(numero_vuelo)


@app.post(
    "/equipaje/reportes",
    response_model=ReporteEquipaje,
    status_code=status.HTTP_201_CREATED,
    summary="Reportar inconvenientes con equipaje",
)
def reportar_inconveniente_equipaje(entrada: ReporteEquipajeEntrada) -> ReporteEquipaje:
    return registrar_reporte_equipaje(entrada)
