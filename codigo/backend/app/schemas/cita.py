from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import EstadoCita
from app.schemas.barbero import BarberoOut
from app.schemas.servicio import ServicioOut


class CitaIn(BaseModel):
    barbero_id: int
    servicio_id: int
    inicio: datetime


class CitaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    inicio: datetime
    fin: datetime
    estado: EstadoCita
    barbero: BarberoOut
    servicio: ServicioOut
