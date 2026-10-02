from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.tiempo import a_hora_local, ahora_local
from app.models import Barbero, Cita, EstadoCita, Rol, Usuario
from app.schemas.cita import CitaIn
from app.services import barberos as barberos_service
from app.services import servicios as servicios_service
from app.services.errores import Conflicto, DatosInvalidos, NoEncontrado, PermisoDenegado


def _barbero_del_usuario(db: Session, usuario: Usuario) -> Barbero | None:
    return db.scalar(select(Barbero).where(Barbero.usuario_id == usuario.id))


def crear(db: Session, cliente: Usuario, datos: CitaIn) -> Cita:
    inicio = a_hora_local(datos.inicio).replace(second=0, microsecond=0)
    if inicio <= ahora_local():
        raise DatosInvalidos("No se puede agendar una cita en el pasado")

    # Bloquea la fila del barbero para serializar reservas concurrentes (PostgreSQL)
    barbero = db.scalar(
        select(Barbero).where(Barbero.id == datos.barbero_id, Barbero.activo.is_(True)).with_for_update()
    )
    if barbero is None:
        raise NoEncontrado("Barbero no encontrado")
    servicio = servicios_service.obtener(db, datos.servicio_id)
    if not servicio.activo:
        raise DatosInvalidos("El servicio no está disponible")

    fin =inicio + timedelta(minutes=servicio.duracion_minutos)
    fecha = inicio.date()
    if (
        fin.date() != fecha
        or inicio < datetime.combine(fecha, barbero.hora_inicio)
        or fin > datetime.combine(fecha, barbero.hora_fin)
    ):
        raise DatosInvalidos("La cita está fuera del horario del barbero")

    for existente in barberos_service.citas_activas_del_dia(db, barbero.id, fecha):
        if existente.inicio < fin and inicio < existente.fin:
            raise Conflicto("El barbero ya tiene una cita en ese horario")

    cita = Cita(cliente_id=cliente.id, barbero_id=barbero.id, servicio_id=servicio.id, inicio=inicio, fin=fin)
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


def listar(db: Session, usuario: Usuario) -> list[Cita]:
    """Admin: todas. Barbero: su agenda. Cliente: sus propias citas."""
    consulta = select(Cita).order_by(Cita.inicio)
    if usuario.rol == Rol.BARBERO:
        barbero = _barbero_del_usuario(db, usuario)
        if barbero is None:
            return []
        consulta = consulta.where(Cita.barbero_id == barbero.id)
    elif usuario.rol == Rol.CLIENTE:
        consulta = consulta.where(Cita.cliente_id == usuario.id)
    return list(db.scalars(consulta))


def cancelar(db: Session, usuario: Usuario, cita_id: int) -> Cita:
    cita = db.get(Cita, cita_id)
    if cita is None:
        raise NoEncontrado("Cita no encontrada")

    if usuario.rol == Rol.CLIENTE and cita.cliente_id != usuario.id:
        raise NoEncontrado("Cita no encontrada")
    if usuario.rol == Rol.BARBERO:
        barbero = _barbero_del_usuario(db, usuario)
        if barbero is None or cita.barbero_id != barbero.id:
            raise PermisoDenegado("La cita no pertenece a tu agenda")

    if cita.estado == EstadoCita.CANCELADA:
        raise Conflicto("La cita ya está cancelada")
    cita.estado = EstadoCita.CANCELADA
    db.commit()
    db.refresh(cita)
    return cita
