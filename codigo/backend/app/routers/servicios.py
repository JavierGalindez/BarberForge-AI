from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.database import get_db
from app.schemas.servicio import ServicioIn, ServicioOut, ServicioUpdate
from app.services import servicios as servicios_service

router = APIRouter(prefix="/servicios", tags=["servicios"])


@router.get("", response_model=list[ServicioOut])
def listar(db: Session = Depends(get_db)):
    return servicios_service.listar(db)


@router.get("/{servicio_id}", response_model=ServicioOut)
def obtener(servicio_id: int, db: Session = Depends(get_db)):
    return servicios_service.obtener(db, servicio_id)


@router.post(
    "", response_model=ServicioOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)]
)
def crear(datos: ServicioIn, db: Session = Depends(get_db)):
    return servicios_service.crear(db, datos)


@router.patch("/{servicio_id}", response_model=ServicioOut, dependencies=[Depends(require_admin)])
def actualizar(servicio_id: int, datos: ServicioUpdate, db: Session = Depends(get_db)):
    return servicios_service.actualizar(db, servicio_id, datos)
