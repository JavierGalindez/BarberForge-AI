def test_registro_login_y_me(client):
    respuesta = client.post(
        "/auth/register", json={"email": "Ana@Test.com", "nombre": "Ana", "password": "secreta123"}
    )
    assert respuesta.status_code == 201
    assert respuesta.json()["rol"] == "cliente"

    login = client.post("/auth/login", data={"username": "ana@test.com", "password": "secreta123"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "ana@test.com"


def test_registro_email_duplicado(client):
    datos = {"email": "ana@test.com", "nombre": "Ana", "password": "secreta123"}
    assert client.post("/auth/register", json=datos).status_code == 201
    assert client.post("/auth/register", json=datos).status_code == 409


def test_login_incorrecto(client):
    respuesta = client.post("/auth/login", data={"username": "nadie@test.com", "password": "xxxxxxxx"})
    assert respuesta.status_code == 401


def test_me_sin_token(client):
    assert client.get("/auth/me").status_code == 401


def test_token_invalido(client):
    assert client.get("/auth/me", headers={"Authorization": "Bearer basura"}).status_code == 401
