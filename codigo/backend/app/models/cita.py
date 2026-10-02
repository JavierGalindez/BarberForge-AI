import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.barbero import Barbero
from app.models.servicio import Servicio
from app.models.usuario import Usuario


class EstadoCita(str, enum.Enum):
    AGENDADA = "agendada"
    CANCELADA = "cancelada"


class Cita(Base):
    __tablename__ = "citas"
    __table_args__ = (Index("ix_citas_barbero_inicio", "barbero_id", "inicio"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    barbero_id: Mapped[int] = mapped_column(ForeignKey("barberos.id"))
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicios.id"))
    # Hora local de la barbería (sin zona horaria)
    inicio: Mapped[datetime] = mapped_column(DateTime)
    fin: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[EstadoCita] = mapped_column(
        Enum(EstadoCita, native_enum=False, length=20, values_callable=lambda e: [m.value for m in e]),
        default=EstadoCita.AGENDADA,
    )
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cliente: Mapped[Usuario] = relationship()
    barbero: Mapped[Barbero] = relationship()
    servicio: Mapped[Servicio] = relationship()
