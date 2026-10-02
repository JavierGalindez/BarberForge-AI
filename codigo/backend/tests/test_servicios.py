SERVICIO = {"nombre": "Fade", "descripcion": "Degradado", "precio": "30000", "duracion_minutos": 45}


def test_listar_servicios_publico(client, servicio):
    respuesta = client.get("/servicios")
    assert respuesta.status_code == 200
    assert [s["nombre"] for s in respuesta.json()] == ["Corte"]


def test_crear_servicio_requiere_admin(client, cliente_headers):
    assert client.post("/servicios", json=SERVICIO).status_code == 401
    assert client.post("/servicios", json=SERVICIO, headers=cliente_headers).status_code == 403


def test_admin_crea_y_actualiza_servicio(client, admin_headers):
    creado = client.post("/servicios", json=SERVICIO, headers=admin_headers)
    assert creado.status_code == 201
    servicio_id = creado.json()["id"]

    actualizado = client.patch(f"/servicios/{servicio_id}", json={"activo": False}, headers=admin_headers)
    assert actualizado.status_code == 200
    assert client.get("/servicios").json() == []


def test_nombre_duplicado(client, admin_headers):
    assert client.post("/servicios", json=SERVICIO, headers=admin_headers).status_code == 201
    assert client.post("/servicios", json=SERVICIO, headers=admin_headers).status_code == 409


def test_servicio_inexistente(client):
    assert client.get("/servicios/999").status_code == 404
