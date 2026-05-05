from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status

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

app = FastAPI(
    title="FlyTrack API",
    description="Backend de AeroPuerto Smart para itinerarios, notificaciones, puertas de embarque y reportes de equipaje.",
    version="1.0.0",
)


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
