FECHA = "2030-01-15"


def _cita(barbero, servicio, hora: str) -> dict:
    return {"barbero_id": barbero.id, "servicio_id": servicio.id, "inicio": f"{FECHA}T{hora}"}


def test_crear_cita(client, barbero, servicio, cliente_headers):
    respuesta = client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=cliente_headers)
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["fin"] == f"{FECHA}T10:00:00"
    assert cuerpo["estado"] == "agendada"
    assert cuerpo["servicio"]["nombre"] == "Corte"


def test_crear_cita_requiere_login(client, barbero, servicio):
    assert client.post("/citas", json=_cita(barbero, servicio, "09:00:00")).status_code == 401


def test_no_se_permiten_citas_solapadas(client, barbero, servicio, cliente_headers, otro_cliente_headers):
    assert client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=cliente_headers).status_code == 201
    respuesta = client.post("/citas", json=_cita(barbero, servicio, "09:30:00"), headers=otro_cliente_headers)
    assert respuesta.status_code == 409


def test_citas_contiguas_si_se_permiten(client, barbero, servicio, cliente_headers):
    assert client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=cliente_headers).status_code == 201
    assert client.post("/citas", json=_cita(barbero, servicio, "10:00:00"), headers=cliente_headers).status_code == 201


def test_cita_fuera_de_horario(client, barbero, servicio, cliente_headers):
    # Jornada hasta las 12:00 y el servicio dura 60 min
    respuesta = client.post("/citas", json=_cita(barbero, servicio, "11:30:00"), headers=cliente_headers)
    assert respuesta.status_code == 422
    respuesta = client.post("/citas", json=_cita(barbero, servicio, "08:00:00"), headers=cliente_headers)
    assert respuesta.status_code == 422


def test_cancelar_libera_el_horario(client, barbero, servicio, cliente_headers, otro_cliente_headers):
    cita = client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=cliente_headers).json()

    cancelada = client.post(f"/citas/{cita['id']}/cancelar", headers=cliente_headers)
    assert cancelada.status_code == 200
    assert cancelada.json()["estado"] == "cancelada"
    assert client.post(f"/citas/{cita['id']}/cancelar", headers=cliente_headers).status_code == 409

    respuesta = client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=otro_cliente_headers)
    assert respuesta.status_code == 201


def test_cliente_solo_ve_y_cancela_sus_citas(client, barbero, servicio, cliente_headers, otro_cliente_headers):
    cita = client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=cliente_headers).json()

    assert len(client.get("/citas", headers=cliente_headers).json()) == 1
    assert client.get("/citas", headers=otro_cliente_headers).json() == []
    assert client.post(f"/citas/{cita['id']}/cancelar", headers=otro_cliente_headers).status_code == 404


def test_barbero_ve_y_cancela_su_agenda(client, admin_headers, servicio, cliente_headers):
    datos = {"nombre": "Luis", "hora_inicio": "09:00", "hora_fin": "17:00", "email": "luis@test.com", "password": "barbero123"}
    barbero_id = client.post("/barberos", json=datos, headers=admin_headers).json()["id"]
    login = client.post("/auth/login", data={"username": "luis@test.com", "password": "barbero123"})
    barbero_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    cita = client.post(
        "/citas",
        json={"barbero_id": barbero_id, "servicio_id": servicio.id, "inicio": f"{FECHA}T09:00:00"},
        headers=cliente_headers,
    ).json()

    agenda = client.get("/citas", headers=barbero_headers).json()
    assert [c["id"] for c in agenda] == [cita["id"]]
    assert client.post(f"/citas/{cita['id']}/cancelar", headers=barbero_headers).status_code == 200


def test_barbero_no_cancela_citas_ajenas(client, admin_headers, barbero, servicio, cliente_headers):
    datos = {"nombre": "Luis", "hora_inicio": "09:00", "hora_fin": "17:00", "email": "luis@test.com", "password": "barbero123"}
    client.post("/barberos", json=datos, headers=admin_headers)
    login = client.post("/auth/login", data={"username": "luis@test.com", "password": "barbero123"})
    barbero_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    cita = client.post("/citas", json=_cita(barbero, servicio, "09:00:00"), headers=cliente_headers).json()
    assert client.post(f"/citas/{cita['id']}/cancelar", headers=barbero_headers).status_code == 403


def test_no_se_agenda_en_el_pasado(client, barbero, servicio, cliente_headers):
    cita = {"barbero_id": barbero.id, "servicio_id": servicio.id, "inicio": "2020-01-15T09:00:00"}
    respuesta = client.post("/citas", json=cita, headers=cliente_headers)
    assert respuesta.status_code == 422
    assert "pasado" in respuesta.json()["detail"]


def test_hora_con_zona_se_convierte_a_hora_de_colombia(client, barbero, servicio, cliente_headers):
    # 14:00 UTC = 09:00 en Bogotá (UTC-5)
    cita = {"barbero_id": barbero.id, "servicio_id": servicio.id, "inicio": f"{FECHA}T14:00:00Z"}
    respuesta = client.post("/citas", json=cita, headers=cliente_headers)
    assert respuesta.status_code == 201
    assert respuesta.json()["inicio"] == f"{FECHA}T09:00:00"
