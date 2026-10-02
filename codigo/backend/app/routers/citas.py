from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database import get_db
from app.models import Rol, Usuario
from app.schemas.cita import CitaIn, CitaOut
from app.services import citas as citas_service

router = APIRouter(prefix="/citas", tags=["citas"])


@router.post("", response_model=CitaOut, status_code=status.HTTP_201_CREATED)
def crear(
    datos: CitaIn,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_roles(Rol.CLIENTE, Rol.ADMIN)),
):
    return citas_service.crear(db, usuario, datos)


@router.get("", response_model=list[CitaOut])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    return citas_service.listar(db, usuario)


@router.post("/{cita_id}/cancelar", response_model=CitaOut)
def cancelar(cita_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    return citas_service.cancelar(db, usuario, cita_id)
