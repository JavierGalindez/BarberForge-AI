# 004 — Plan

> Cómo se implementa.

## Enfoque técnico
- Instalar el stack con Helm: OTel Collector, kube-prometheus-stack, Tempo y Loki.
- Autoinstrumentación de OTel para Python y Node.js, más métricas propias (`consultas_totales`, `latencia_llm_segundos`, `cola_redis_tamano`).
- Dashboard de Grafana versionado como JSON en el repositorio.

## Componentes
- `codigo/observabilidad/`
- Instrumentación en `codigo/gateway/`, `codigo/ia/` y `codigo/whatsapp-bot/`
