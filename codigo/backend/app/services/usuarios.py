from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import Rol, Usuario
from app.services.errores import Conflicto, CredencialesInvalidas


def obtener_por_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email.lower()))


def crear_usuario(
    db: Session, *, email: str, nombre: str, password: str, rol: Rol = Rol.CLIENTE, commit: bool = True
) -> Usuario:
    if obtener_por_email(db, email) is not None:
        raise Conflicto("Ya existe un usuario con ese email")
    usuario = Usuario(email=email.lower(), nombre=nombre, password_hash=hash_password(password), rol=rol)
    db.add(usuario)
    if commit:
        db.commit()
        db.refresh(usuario)
    else:
        db.flush()
    return usuario


def autenticar(db: Session, email: str, password: str) -> str:
    """Devuelve un token de acceso si las credenciales son válidas."""
    usuario = obtener_por_email(db, email)
    if usuario is None or not usuario.activo or not verify_password(password, usuario.password_hash):
        raise CredencialesInvalidas("Email o contraseña incorrectos")
    return create_access_token(usuario.id, usuario.rol.value)


def asegurar_admin(db: Session, email: str, password: str) -> None:
    """Crea el administrador inicial si todavía no existe."""
    if obtener_por_email(db, email) is None:
        crear_usuario(db, email=email, nombre="Administrador", password=password, rol=Rol.ADMIN)
