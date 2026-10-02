"""datos semilla: barberos y catálogo de servicios de ejemplo

Revision ID: 002
Revises: 001
Create Date: 2026-09-30

"""
from datetime import time
from decimal import Decimal
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

barberos = sa.table(
    "barberos",
    sa.column("nombre", sa.String),
    sa.column("hora_inicio", sa.Time),
    sa.column("hora_fin", sa.Time),
    sa.column("activo", sa.Boolean),
)

servicios = sa.table(
    "servicios",
    sa.column("nombre", sa.String),
    sa.column("descripcion", sa.Text),
    sa.column("precio", sa.Numeric),
    sa.column("duracion_minutos", sa.Integer),
    sa.column("activo", sa.Boolean),
)

BARBEROS = [
    {"nombre": "Carlos", "hora_inicio": time(9, 0), "hora_fin": time(18, 0), "activo": True},
    {"nombre": "Andrés", "hora_inicio": time(10, 0), "hora_fin": time(19, 0), "activo": True},
]

SERVICIOS = [
    {"nombre": "Corte clásico", "descripcion": "Corte con tijera y máquina", "precio": Decimal("25000"), "duracion_minutos": 30, "activo": True},
    {"nombre": "Fade", "descripcion": "Degradado con máquina", "precio": Decimal("30000"), "duracion_minutos": 45, "activo": True},
    {"nombre": "Arreglo de barba", "descripcion": "Perfilado y toalla caliente", "precio": Decimal("15000"), "duracion_minutos": 30, "activo": True},
    {"nombre": "Corte + barba", "descripcion": "Corte clásico y arreglo de barba", "precio": Decimal("38000"), "duracion_minutos": 60, "activo": True},
]


def upgrade() -> None:
    op.bulk_insert(barberos, BARBEROS)
    op.bulk_insert(servicios, SERVICIOS)


def downgrade() -> None:
    op.execute(servicios.delete().where(servicios.c.nombre.in_([s["nombre"] for s in SERVICIOS])))
    op.execute(barberos.delete().where(barberos.c.nombre.in_([b["nombre"] for b in BARBEROS])))
