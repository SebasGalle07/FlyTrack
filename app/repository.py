from datetime import datetime
from zoneinfo import ZoneInfo

from app.models import (
    EstadoVuelo,
    Itinerario,
    Notificacion,
    PuertaEmbarque,
    ReporteEquipaje,
    ReporteEquipajeEntrada,
)

ZONA_LOCAL = ZoneInfo("America/Bogota")


itinerarios = [
    Itinerario(
        numero_vuelo="FT101",
        origen="Armenia",
        destino="Bogota",
        salida=datetime(2026, 5, 5, 8, 30, tzinfo=ZONA_LOCAL),
        llegada=datetime(2026, 5, 5, 9, 20, tzinfo=ZONA_LOCAL),
        estado=EstadoVuelo.embarcando,
    ),
    Itinerario(
        numero_vuelo="FT204",
        origen="Armenia",
        destino="Medellin",
        salida=datetime(2026, 5, 5, 10, 15, tzinfo=ZONA_LOCAL),
        llegada=datetime(2026, 5, 5, 11, 5, tzinfo=ZONA_LOCAL),
        estado=EstadoVuelo.retrasado,
    ),
]

puertas = {
    "FT101": PuertaEmbarque(numero_vuelo="FT101", puerta="A3", estado=EstadoVuelo.embarcando),
    "FT204": PuertaEmbarque(numero_vuelo="FT204", puerta="B1", estado=EstadoVuelo.retrasado),
}

notificaciones = [
    Notificacion(
        id=1,
        numero_vuelo="FT204",
        mensaje="El vuelo FT204 presenta cambio de horario por operacion aerea.",
        fecha=datetime(2026, 5, 5, 9, 45, tzinfo=ZONA_LOCAL),
    )
]

reportes_equipaje: list[ReporteEquipaje] = []


def buscar_itinerario(numero_vuelo: str) -> Itinerario | None:
    return next(
        (itinerario for itinerario in itinerarios if itinerario.numero_vuelo == numero_vuelo.upper()),
        None,
    )


def buscar_puerta(numero_vuelo: str) -> PuertaEmbarque | None:
    return puertas.get(numero_vuelo.upper())


def listar_notificaciones(numero_vuelo: str | None = None) -> list[Notificacion]:
    if numero_vuelo is None:
        return notificaciones

    return [
        notificacion
        for notificacion in notificaciones
        if notificacion.numero_vuelo == numero_vuelo.upper()
    ]


def registrar_reporte_equipaje(entrada: ReporteEquipajeEntrada) -> ReporteEquipaje:
    reporte = ReporteEquipaje(
        id=len(reportes_equipaje) + 1,
        numero_vuelo=entrada.numero_vuelo.upper(),
        pasajero=entrada.pasajero,
        codigo_equipaje=entrada.codigo_equipaje,
        tipo=entrada.tipo,
        descripcion=entrada.descripcion,
        fecha_reporte=datetime.now(tz=ZONA_LOCAL),
    )
    reportes_equipaje.append(reporte)
    return reporte


def reiniciar_reportes_equipaje() -> None:
    reportes_equipaje.clear()
