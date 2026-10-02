from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import Rol


class RegistroIn(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=72)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    nombre: str
    rol: Rol


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
