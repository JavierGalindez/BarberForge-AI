FECHA = "2030-01-15"


def test_listar_barberos(client, barbero):
    assert [b["nombre"] for b in client.get("/barberos").json()] == ["Carlos"]


def test_admin_crea_barbero_con_cuenta(client, admin_headers):
    datos = {
        "nombre": "Luis",
        "hora_inicio": "08:00",
        "hora_fin": "16:00",
        "email": "luis@test.com",
        "password": "barbero123",
    }
    assert client.post("/barberos", json=datos, headers=admin_headers).status_code == 201

    login = client.post("/auth/login", data={"username": "luis@test.com", "password": "barbero123"})
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {login.json()['access_token']}"})
    assert me.json()["rol"] == "barbero"


def test_horario_invalido(client, admin_headers):
    datos = {"nombre": "Luis", "hora_inicio": "16:00", "hora_fin": "08:00"}
    assert client.post("/barberos", json=datos, headers=admin_headers).status_code == 422


def test_disponibilidad_jornada_libre(client, barbero, servicio):
    # Jornada 9:00-12:00, servicio de 60 min, intervalo de 30 min
    respuesta = client.get(
        f"/barberos/{barbero.id}/disponibilidad", params={"servicio_id": servicio.id, "fecha": FECHA}
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["horarios"] == [
        f"{FECHA}T09:00:00",
        f"{FECHA}T09:30:00",
        f"{FECHA}T10:00:00",
        f"{FECHA}T10:30:00",
        f"{FECHA}T11:00:00",
    ]


def test_disponibilidad_descuenta_citas(client, barbero, servicio, cliente_headers):
    cita = {"barbero_id": barbero.id, "servicio_id": servicio.id, "inicio": f"{FECHA}T10:00:00"}
    assert client.post("/citas", json=cita, headers=cliente_headers).status_code == 201

    respuesta = client.get(
        f"/barberos/{barbero.id}/disponibilidad", params={"servicio_id": servicio.id, "fecha": FECHA}
    )
    assert respuesta.json()["horarios"] == [f"{FECHA}T09:00:00", f"{FECHA}T11:00:00"]


def test_disponibilidad_barbero_inexistente(client, servicio):
    respuesta = client.get("/barberos/999/disponibilidad", params={"servicio_id": servicio.id, "fecha": FECHA})
    assert respuesta.status_code == 404


def test_disponibilidad_oculta_horas_pasadas(client, barbero, servicio, monkeypatch):
    from datetime import datetime

    from app.services import barberos as barberos_service

    monkeypatch.setattr(barberos_service, "ahora_local", lambda: datetime(2030, 1, 15, 10, 15))
    respuesta = client.get(
        f"/barberos/{barbero.id}/disponibilidad", params={"servicio_id": servicio.id, "fecha": FECHA}
    )
    assert respuesta.json()["horarios"] == [f"{FECHA}T10:30:00", f"{FECHA}T11:00:00"]


def test_disponibilidad_dia_pasado_vacia(client, barbero, servicio):
    respuesta = client.get(
        f"/barberos/{barbero.id}/disponibilidad", params={"servicio_id": servicio.id, "fecha": "2020-01-15"}
    )
    assert respuesta.json()["horarios"] == []
