from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import Usuario
from app.schemas.auth import RegistroIn, TokenOut, UsuarioOut
from app.services import usuarios as usuarios_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(datos: RegistroIn, db: Session = Depends(get_db)):
    return usuarios_service.crear_usuario(db, email=datos.email, nombre=datos.nombre, password=datos.password)


@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # En OAuth2 el campo se llama "username"; aquí contiene el email
    return TokenOut(access_token=usuarios_service.autenticar(db, form.username, form.password))


@router.get("/me", response_model=UsuarioOut)
def yo(usuario: Usuario = Depends(get_current_user)):
    return usuario
