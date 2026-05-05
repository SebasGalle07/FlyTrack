from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class EstadoVuelo(str, Enum):
    programado = "programado"
    retrasado = "retrasado"
    embarcando = "embarcando"
    cancelado = "cancelado"


class TipoEquipaje(str, Enum):
    perdido = "perdido"
    danado = "danado"
    retrasado = "retrasado"


class Itinerario(BaseModel):
    numero_vuelo: str = Field(..., examples=["FT101"])
    origen: str = Field(..., examples=["Armenia"])
    destino: str = Field(..., examples=["Bogota"])
    salida: datetime
    llegada: datetime
    estado: EstadoVuelo


class PuertaEmbarque(BaseModel):
    numero_vuelo: str = Field(..., examples=["FT101"])
    puerta: str = Field(..., examples=["A3"])
    estado: EstadoVuelo


class Notificacion(BaseModel):
    id: int
    numero_vuelo: str = Field(..., examples=["FT101"])
    tipo: Literal["cambio_vuelo"] = "cambio_vuelo"
    mensaje: str
    fecha: datetime


class ReporteEquipajeEntrada(BaseModel):
    numero_vuelo: str = Field(..., examples=["FT101"])
    pasajero: str = Field(..., examples=["Sebastian Perez"])
    codigo_equipaje: str = Field(..., examples=["BAG-4589"])
    tipo: TipoEquipaje
    descripcion: str = Field(..., min_length=5, examples=["La maleta no llego en la banda."])


class ReporteEquipaje(BaseModel):
    id: int
    numero_vuelo: str
    pasajero: str
    codigo_equipaje: str
    tipo: TipoEquipaje
    descripcion: str
    estado: Literal["recibido"] = "recibido"
    fecha_reporte: datetime


class ErrorRespuesta(BaseModel):
    detail: str
