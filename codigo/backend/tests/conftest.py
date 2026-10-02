import os

# Valores por defecto para ejecutar los tests fuera de Docker; en el contenedor ya vienen del entorno.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET", "test-secret")

from datetime import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Barbero, Rol, Servicio
from app.services import usuarios as usuarios_service

# BD de pruebas en memoria, aislada de la base de datos real
engine_pruebas = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
SesionPruebas = sessionmaker(bind=engine_pruebas, autoflush=False, expire_on_commit=False)


@pytest.fixture
def db():
    Base.metadata.create_all(engine_pruebas)
    sesion = SesionPruebas()
    try:
        yield sesion
    finally:
        sesion.close()
        Base.metadata.drop_all(engine_pruebas)


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    # Sin "with": no se ejecuta el lifespan, así que no se toca la BD real
    yield TestClient(app)
    app.dependency_overrides.clear()


def _token(client: TestClient, email: str, password: str) -> dict[str, str]:
    respuesta = client.post("/auth/login", data={"username": email, "password": password})
    assert respuesta.status_code == 200, respuesta.text
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}


@pytest.fixture
def admin_headers(client, db):
    usuarios_service.crear_usuario(db, email="admin@test.com", nombre="Admin", password="admin12345", rol=Rol.ADMIN)
    return _token(client, "admin@test.com", "admin12345")


@pytest.fixture
def cliente_headers(client, db):
    usuarios_service.crear_usuario(db, email="cliente@test.com", nombre="Cliente", password="cliente12345")
    return _token(client, "cliente@test.com", "cliente12345")


@pytest.fixture
def otro_cliente_headers(client, db):
    usuarios_service.crear_usuario(db, email="otro@test.com", nombre="Otro", password="otro123456")
    return _token(client, "otro@test.com", "otro123456")


@pytest.fixture
def barbero(db) -> Barbero:
    barbero = Barbero(nombre="Carlos", hora_inicio=time(9, 0), hora_fin=time(12, 0), activo=True)
    db.add(barbero)
    db.commit()
    return barbero


@pytest.fixture
def servicio(db) -> Servicio:
    servicio = Servicio(nombre="Corte", precio=25000, duracion_minutos=60, activo=True)
    db.add(servicio)
    db.commit()
    return servicio
