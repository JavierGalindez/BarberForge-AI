from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.core.deps import require_admin
from app.database import get_db
from app.schemas.barbero import BarberoIn, BarberoOut, DisponibilidadOut
from app.services import barberos as barberos_service

router = APIRouter(prefix="/barberos", tags=["barberos"])


@router.get("", response_model=list[BarberoOut])
def listar(db: Session = Depends(get_db)):
    return barberos_service.listar(db)


@router.get("/{barbero_id}", response_model=BarberoOut)
def obtener(barbero_id: int, db: Session = Depends(get_db)):
    return barberos_service.obtener(db, barbero_id)


@router.post(
    "", response_model=BarberoOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)]
)
def crear(datos: BarberoIn, db: Session = Depends(get_db)):
    return barberos_service.crear(db, datos)


@router.get("/{barbero_id}/disponibilidad", response_model=DisponibilidadOut)
def disponibilidad(
    barbero_id: int,
    servicio_id: int,
    fecha: date,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    horarios = barberos_service.disponibilidad(
        db, barbero_id, servicio_id, fecha, settings.AGENDA_INTERVALO_MINUTOS
    )
    return DisponibilidadOut(barbero_id=barbero_id, servicio_id=servicio_id, fecha=fecha, horarios=horarios)
