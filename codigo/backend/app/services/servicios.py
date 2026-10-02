from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Servicio
from app.schemas.servicio import ServicioIn, ServicioUpdate
from app.services.errores import Conflicto, NoEncontrado


def listar(db: Session, incluir_inactivos: bool = False) -> list[Servicio]:
    consulta = select(Servicio).order_by(Servicio.nombre)
    if not incluir_inactivos:
        consulta = consulta.where(Servicio.activo.is_(True))
    return list(db.scalars(consulta))


def obtener(db: Session, servicio_id: int) -> Servicio:
    servicio = db.get(Servicio, servicio_id)
    if servicio is None:
        raise NoEncontrado("Servicio no encontrado")
    return servicio


def _validar_nombre_unico(db: Session, nombre: str, excluir_id: int | None = None) -> None:
    existente = db.scalar(select(Servicio).where(Servicio.nombre == nombre))
    if existente is not None and existente.id != excluir_id:
        raise Conflicto("Ya existe un servicio con ese nombre")


def crear(db: Session, datos: ServicioIn) -> Servicio:
    _validar_nombre_unico(db, datos.nombre)
    servicio = Servicio(**datos.model_dump())
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio


def actualizar(db: Session, servicio_id: int, datos: ServicioUpdate) -> Servicio:
    servicio = obtener(db, servicio_id)
    cambios = datos.model_dump(exclude_unset=True)
    if "nombre" in cambios:
        _validar_nombre_unico(db, cambios["nombre"], excluir_id=servicio.id)
    for campo, valor in cambios.items():
        setattr(servicio, campo, valor)
    db.commit()
    db.refresh(servicio)
    return servicio
