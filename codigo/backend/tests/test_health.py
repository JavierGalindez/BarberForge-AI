def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_health_db(client):
    respuesta = client.get("/health/db")
    assert respuesta.status_code == 200
    assert respuesta.json()["database"] == "ok"
