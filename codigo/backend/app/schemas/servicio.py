from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ServicioIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str | None = None
    precio: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    duracion_minutos: int = Field(gt=0, le=480)


class ServicioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    descripcion: str | None = None
    precio: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    duracion_minutos: int | None = Field(default=None, gt=0, le=480)
    activo: bool | None = None


class ServicioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    precio: Decimal
    duracion_minutos: int
    activo: bool
