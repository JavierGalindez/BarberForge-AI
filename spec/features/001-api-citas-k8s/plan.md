# 001 — Plan

> Cómo se implementa.

## Enfoque técnico
- Gateway en Django + DRF (o FastAPI, según la decisión del roadmap) en `codigo/gateway/`.
- Modelos: `Barbero`, `Servicio` (nombre, precio, duración), `Cita` (cliente, barbero, servicio, inicio, fin, estado).
- La disponibilidad se calcula a partir del horario laboral del barbero menos las citas existentes.
- Dockerfile multi-stage, usuario no root.
- Helm chart en `codigo/helm/barberforge/` con PostgreSQL (imagen `pgvector/pgvector`) y Redis.

## Componentes
- `codigo/gateway/`
- `codigo/helm/barberforge/`
- Datos semilla: barberos y catálogo de servicios de ejemplo.
