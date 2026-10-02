from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import get_settings


def zona_barberia() -> ZoneInfo:
    return ZoneInfo(get_settings().ZONA_HORARIA)


def ahora_local() -> datetime:
    """Fecha y hora actual de la barbería, sin zona horaria (igual que las citas en la BD)."""
    return datetime.now(zona_barberia()).replace(tzinfo=None)


def a_hora_local(momento: datetime) -> datetime:
    """Convierte un datetime con zona horaria a la hora local de la barbería; los ingenuos se dejan igual."""
    if momento.tzinfo is None:
        return momento
    return momento.astimezone(zona_barberia()).replace(tzinfo=None)
