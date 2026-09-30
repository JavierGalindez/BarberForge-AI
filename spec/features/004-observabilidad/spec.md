# 004 — Observabilidad y SRE

> Qué hace esta feature y criterios de aceptación.

## Descripción
Instrumentar los servicios con OpenTelemetry y visualizar métricas, trazas y logs en Grafana.

## Criterios de aceptación
- [ ] Gateway, servicio de IA y bot envían telemetría al OpenTelemetry Collector.
- [ ] Prometheus, Tempo y Loki reciben métricas, trazas y logs.
- [ ] Un dashboard de Grafana muestra: consultas atendidas por el bot, latencia de respuesta del modelo, tamaño de la cola de Redis, CPU y memoria del nodo.
- [ ] Una petición de chat se puede seguir de punta a punta en una traza (gateway → IA → Ollama → BD).
- [ ] (Si hay GPU NVIDIA) el exportador DCGM muestra el uso de VRAM.
