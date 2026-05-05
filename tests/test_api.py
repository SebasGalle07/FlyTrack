from fastapi.testclient import TestClient

from app.main import app
from app.repository import reiniciar_reportes_equipaje

client = TestClient(app)


def setup_function() -> None:
    reiniciar_reportes_equipaje()


# ─────────────────────────────────────────────
# GET /itinerarios
# ─────────────────────────────────────────────


def test_itinerarios_retorna_200() -> None:
    response = client.get("/itinerarios")
    assert response.status_code == 200


def test_itinerarios_retorna_lista_completa() -> None:
    response = client.get("/itinerarios")
    assert len(response.json()) == 2


def test_itinerarios_contiene_ft101() -> None:
    response = client.get("/itinerarios")
    numeros = [v["numero_vuelo"] for v in response.json()]
    assert "FT101" in numeros


def test_itinerarios_contiene_ft204() -> None:
    response = client.get("/itinerarios")
    numeros = [v["numero_vuelo"] for v in response.json()]
    assert "FT204" in numeros


def test_itinerarios_estructura_campos() -> None:
    response = client.get("/itinerarios")
    vuelo = response.json()[0]
    for campo in ("numero_vuelo", "origen", "destino", "salida", "llegada", "estado"):
        assert campo in vuelo


# ─────────────────────────────────────────────
# GET /itinerarios/{numero_vuelo}
# ─────────────────────────────────────────────


def test_itinerario_ft101_retorna_200() -> None:
    response = client.get("/itinerarios/FT101")
    assert response.status_code == 200


def test_itinerario_ft101_datos_correctos() -> None:
    response = client.get("/itinerarios/FT101")
    data = response.json()
    assert data["numero_vuelo"] == "FT101"
    assert data["origen"] == "Armenia"
    assert data["destino"] == "Bogota"
    assert data["estado"] == "embarcando"


def test_itinerario_ft204_retorna_200() -> None:
    response = client.get("/itinerarios/FT204")
    assert response.status_code == 200


def test_itinerario_ft204_datos_correctos() -> None:
    response = client.get("/itinerarios/FT204")
    data = response.json()
    assert data["numero_vuelo"] == "FT204"
    assert data["origen"] == "Armenia"
    assert data["destino"] == "Medellin"
    assert data["estado"] == "retrasado"


def test_itinerario_busqueda_case_insensitive() -> None:
    response = client.get("/itinerarios/ft101")
    assert response.status_code == 200
    assert response.json()["numero_vuelo"] == "FT101"


def test_itinerario_no_encontrado_retorna_404() -> None:
    response = client.get("/itinerarios/ZZZZZZ")
    assert response.status_code == 404


def test_itinerario_no_encontrado_mensaje_error() -> None:
    response = client.get("/itinerarios/VUELO_NO_EXISTE")
    assert response.json()["detail"] == "Vuelo no encontrado"


# ─────────────────────────────────────────────
# GET /puertas-embarque/{numero_vuelo}
# ─────────────────────────────────────────────


def test_puerta_ft101_retorna_200() -> None:
    response = client.get("/puertas-embarque/FT101")
    assert response.status_code == 200


def test_puerta_ft101_datos_correctos() -> None:
    response = client.get("/puertas-embarque/FT101")
    data = response.json()
    assert data["numero_vuelo"] == "FT101"
    assert data["puerta"] == "A3"
    assert data["estado"] == "embarcando"


def test_puerta_ft204_retorna_200() -> None:
    response = client.get("/puertas-embarque/FT204")
    assert response.status_code == 200


def test_puerta_ft204_datos_correctos() -> None:
    response = client.get("/puertas-embarque/FT204")
    data = response.json()
    assert data["numero_vuelo"] == "FT204"
    assert data["puerta"] == "B1"
    assert data["estado"] == "retrasado"


def test_puerta_busqueda_case_insensitive() -> None:
    response = client.get("/puertas-embarque/ft101")
    assert response.status_code == 200
    assert response.json()["puerta"] == "A3"


def test_puerta_no_encontrada_retorna_404() -> None:
    response = client.get("/puertas-embarque/ZZZZZZ")
    assert response.status_code == 404


def test_puerta_no_encontrada_mensaje_error() -> None:
    response = client.get("/puertas-embarque/VUELO_NO_EXISTE")
    assert response.json()["detail"] == "Puerta no encontrada"


def test_puerta_estructura_campos() -> None:
    response = client.get("/puertas-embarque/FT101")
    data = response.json()
    for campo in ("numero_vuelo", "puerta", "estado"):
        assert campo in data


# ─────────────────────────────────────────────
# GET /notificaciones
# ─────────────────────────────────────────────


def test_notificaciones_retorna_200() -> None:
    response = client.get("/notificaciones")
    assert response.status_code == 200


def test_notificaciones_retorna_lista_no_vacia() -> None:
    response = client.get("/notificaciones")
    assert len(response.json()) >= 1


def test_notificaciones_filtro_ft204_retorna_1() -> None:
    response = client.get("/notificaciones", params={"numero_vuelo": "FT204"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["numero_vuelo"] == "FT204"


def test_notificaciones_filtro_ft101_retorna_vacio() -> None:
    # FT101 no tiene notificaciones en los datos iniciales
    response = client.get("/notificaciones", params={"numero_vuelo": "FT101"})
    assert response.status_code == 200
    assert response.json() == []


def test_notificaciones_filtro_vuelo_inexistente_retorna_vacio() -> None:
    response = client.get("/notificaciones", params={"numero_vuelo": "ZZZZZZ"})
    assert response.status_code == 200
    assert response.json() == []


def test_notificaciones_filtro_case_insensitive() -> None:
    response = client.get("/notificaciones", params={"numero_vuelo": "ft204"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_notificaciones_estructura_campos() -> None:
    response = client.get("/notificaciones")
    notificacion = response.json()[0]
    for campo in ("id", "numero_vuelo", "tipo", "mensaje", "fecha"):
        assert campo in notificacion


def test_notificaciones_tipo_es_cambio_vuelo() -> None:
    response = client.get("/notificaciones")
    assert response.json()[0]["tipo"] == "cambio_vuelo"


# ─────────────────────────────────────────────
# POST /equipaje/reportes
# ─────────────────────────────────────────────

_PAYLOAD_VALIDO = {
    "numero_vuelo": "FT101",
    "pasajero": "Sebastian Perez",
    "codigo_equipaje": "BAG-4589",
    "tipo": "perdido",
    "descripcion": "La maleta no llego en la banda.",
}


def test_equipaje_retorna_201() -> None:
    response = client.post("/equipaje/reportes", json=_PAYLOAD_VALIDO)
    assert response.status_code == 201


def test_equipaje_primer_id_es_1() -> None:
    response = client.post("/equipaje/reportes", json=_PAYLOAD_VALIDO)
    assert response.json()["id"] == 1


def test_equipaje_estado_recibido() -> None:
    response = client.post("/equipaje/reportes", json=_PAYLOAD_VALIDO)
    assert response.json()["estado"] == "recibido"


def test_equipaje_numero_vuelo_se_guarda_en_mayusculas() -> None:
    payload = {**_PAYLOAD_VALIDO, "numero_vuelo": "ft101"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.json()["numero_vuelo"] == "FT101"


def test_equipaje_ids_autoincremento() -> None:
    r1 = client.post("/equipaje/reportes", json=_PAYLOAD_VALIDO)
    r2 = client.post("/equipaje/reportes", json=_PAYLOAD_VALIDO)
    assert r1.json()["id"] == 1
    assert r2.json()["id"] == 2


def test_equipaje_tipo_danado() -> None:
    payload = {**_PAYLOAD_VALIDO, "tipo": "danado"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 201
    assert response.json()["tipo"] == "danado"


def test_equipaje_tipo_retrasado() -> None:
    payload = {**_PAYLOAD_VALIDO, "tipo": "retrasado"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 201
    assert response.json()["tipo"] == "retrasado"


def test_equipaje_estructura_campos() -> None:
    response = client.post("/equipaje/reportes", json=_PAYLOAD_VALIDO)
    data = response.json()
    for campo in ("id", "numero_vuelo", "pasajero", "codigo_equipaje", "tipo", "descripcion", "estado", "fecha_reporte"):
        assert campo in data


def test_equipaje_datos_guardados_correctamente() -> None:
    payload = {
        "numero_vuelo": "FT204",
        "pasajero": "Maria Lopez",
        "codigo_equipaje": "BAG-9999",
        "tipo": "danado",
        "descripcion": "La rueda de la maleta esta rota.",
    }
    response = client.post("/equipaje/reportes", json=payload)
    data = response.json()
    assert data["numero_vuelo"] == "FT204"
    assert data["pasajero"] == "Maria Lopez"
    assert data["codigo_equipaje"] == "BAG-9999"
    assert data["tipo"] == "danado"
    assert data["descripcion"] == "La rueda de la maleta esta rota."


def test_equipaje_descripcion_muy_corta_retorna_422() -> None:
    payload = {**_PAYLOAD_VALIDO, "descripcion": "abc"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422


def test_equipaje_descripcion_vacia_retorna_422() -> None:
    payload = {**_PAYLOAD_VALIDO, "descripcion": ""}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422


def test_equipaje_tipo_invalido_retorna_422() -> None:
    payload = {**_PAYLOAD_VALIDO, "tipo": "extraviado"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422


def test_equipaje_sin_numero_vuelo_retorna_422() -> None:
    payload = {k: v for k, v in _PAYLOAD_VALIDO.items() if k != "numero_vuelo"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422


def test_equipaje_sin_pasajero_retorna_422() -> None:
    payload = {k: v for k, v in _PAYLOAD_VALIDO.items() if k != "pasajero"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422


def test_equipaje_sin_descripcion_retorna_422() -> None:
    payload = {k: v for k, v in _PAYLOAD_VALIDO.items() if k != "descripcion"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422


def test_equipaje_sin_codigo_equipaje_retorna_422() -> None:
    payload = {k: v for k, v in _PAYLOAD_VALIDO.items() if k != "codigo_equipaje"}
    response = client.post("/equipaje/reportes", json=payload)
    assert response.status_code == 422
