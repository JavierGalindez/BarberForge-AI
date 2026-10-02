from datetime import time

from sqlalchemy import Boolean, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.usuario import Usuario


class Barbero(Base):
    __tablename__ = "barberos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    hora_inicio: Mapped[time] = mapped_column(Time)
    hora_fin: Mapped[time] = mapped_column(Time)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    # Cuenta con la que el barbero inicia sesión para ver su agenda (opcional)
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), unique=True, nullable=True
    )

    usuario: Mapped[Usuario | None] = relationship()
