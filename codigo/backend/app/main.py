from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal, get_db
from app.routers import auth, barberos, citas, servicios
from app.services import usuarios as usuarios_service
from app.services.errores import (
    Conflicto,
    CredencialesInvalidas,
    DatosInvalidos,
    ErrorDominio,
    NoEncontrado,
    PermisoDenegado,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD:
        with SessionLocal() as db:
            usuarios_service.asegurar_admin(db, settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_CODIGOS_HTTP = {
    NoEncontrado: status.HTTP_404_NOT_FOUND,
    Conflicto: status.HTTP_409_CONFLICT,
    DatosInvalidos: status.HTTP_422_UNPROCESSABLE_CONTENT,
    PermisoDenegado: status.HTTP_403_FORBIDDEN,
    CredencialesInvalidas: status.HTTP_401_UNAUTHORIZED,
}


@app.exception_handler(ErrorDominio)
async def manejar_error_dominio(_: Request, exc: ErrorDominio) -> JSONResponse:
    codigo = _CODIGOS_HTTP.get(type(exc), status.HTTP_400_BAD_REQUEST)
    return JSONResponse(status_code=codigo, content={"detail": exc.mensaje})


app.include_router(auth.router)
app.include_router(servicios.router)
app.include_router(barberos.router)
app.include_router(citas.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/health/db", tags=["health"])
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"status": "error", "database": "unreachable"}
        )
    return {"status": "ok", "database": "ok"}
