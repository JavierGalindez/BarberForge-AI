from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class BarberoIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    hora_inicio: time
    hora_fin: time
    # Si se envían, se crea una cuenta con rol "barbero" vinculada
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=72)

    @model_validator(mode="after")
    def validar(self) -> "BarberoIn":
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("hora_fin debe ser posterior a hora_inicio")
        if (self.email is None) != (self.password is None):
            raise ValueError("email y password deben enviarse juntos")
        return self


class BarberoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    hora_inicio: time
    hora_fin: time
    activo: bool


class DisponibilidadOut(BaseModel):
    barbero_id: int
    servicio_id: int
    fecha: date
    horarios: list[datetime]
