from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "BarberForge API"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    # Orígenes permitidos por CORS, separados por coma
    CORS_ORIGINS: str = "http://localhost:3000"
    # Zona horaria de la barbería: las citas se guardan en esta hora local
    ZONA_HORARIA: str = "America/Bogota"
    # Paso entre los horarios ofrecidos en la disponibilidad
    AGENDA_INTERVALO_MINUTOS: int = 30
    # Administrador inicial (opcional): se crea al arrancar si no existe
    ADMIN_EMAIL: str | None = None
    ADMIN_PASSWORD: str | None = None

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
