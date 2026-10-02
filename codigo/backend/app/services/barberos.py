from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.tiempo import ahora_local
from app.models import Barbero, Cita, EstadoCita, Rol
from app.schemas.barbero import BarberoIn
from app.services import servicios as servicios_service
from app.services import usuarios as usuarios_service
from app.services.errores import NoEncontrado


def listar(db: Session) -> list[Barbero]:
    return list(db.scalars(select(Barbero).where(Barbero.activo.is_(True)).order_by(Barbero.nombre)))


def obtener(db: Session, barbero_id: int) -> Barbero:
    barbero = db.get(Barbero, barbero_id)
    if barbero is None or not barbero.activo:
        raise NoEncontrado("Barbero no encontrado")
    return barbero


def crear(db: Session, datos: BarberoIn) -> Barbero:
    barbero = Barbero(nombre=datos.nombre, hora_inicio=datos.hora_inicio, hora_fin=datos.hora_fin)
    if datos.email is not None and datos.password is not None:
        barbero.usuario = usuarios_service.crear_usuario(
            db, email=datos.email, nombre=datos.nombre, password=datos.password, rol=Rol.BARBERO, commit=False
        )
    db.add(barbero)
    db.commit()
    db.refresh(barbero)
    return barbero


def citas_activas_del_dia(db: Session, barbero_id: int, fecha: date) -> list[Cita]:
    desde = datetime.combine(fecha, datetime.min.time())
    hasta = desde + timedelta(days=1)
    consulta = select(Cita).where(
        Cita.barbero_id == barbero_id,
        Cita.estado == EstadoCita.AGENDADA,
        Cita.inicio < hasta,
        Cita.fin > desde,
    )
    return list(db.scalars(consulta))


def disponibilidad(
    db: Session, barbero_id: int, servicio_id: int, fecha: date, intervalo_minutos: int
) -> list[datetime]:
    """Horarios de inicio libres: jornada del barbero menos las citas ya agendadas y las horas ya pasadas."""
    barbero = obtener(db, barbero_id)
    servicio = servicios_service.obtener(db, servicio_id)
    duracion = timedelta(minutes=servicio.duracion_minutos)
    paso = timedelta(minutes=intervalo_minutos)

    jornada_inicio = datetime.combine(fecha, barbero.hora_inicio)
    jornada_fin = datetime.combine(fecha, barbero.hora_fin)
    ocupados = [(c.inicio, c.fin) for c in citas_activas_del_dia(db, barbero.id, fecha)]

    ahora = ahora_local()

    libres: list[datetime] = []
    actual = jornada_inicio
    while actual + duracion <= jornada_fin:
        fin = actual + duracion
        if actual > ahora and all(not (inicio < fin and actual < termino) for inicio, termino in ocupados):
            libres.append(actual)
        actual += paso
    return libres
