# Roadmap

> Orden de las features. Se construye por fases para no llegar a la entrega con todo a medias; lo más riesgoso va al final.

| # | Feature | Objetivo |
|---|---|---|
| 1 | [001-api-citas-k8s](../features/001-api-citas-k8s/spec.md) | Esqueleto del repo, API y base de datos de citas desplegadas en Kubernetes con Helm |
| 2 | [002-cicd-devsecops](../features/002-cicd-devsecops/spec.md) | Pipeline con Trivy, SBOM, Cosign y despliegue con Argo CD |
| 3 | [003-chat-web-rag](../features/003-chat-web-rag/spec.md) | Chat web con Ollama, RAG y tool calling para las citas |
| 4 | [004-observabilidad](../features/004-observabilidad/spec.md) | OpenTelemetry y dashboards de Grafana |
| 5 | [005-bot-whatsapp](../features/005-bot-whatsapp/spec.md) | Bot de WhatsApp conectado al asistente |
| 6 | [006-corte-por-referencia](../features/006-corte-por-referencia/spec.md) | Flujo multimodal: foto de referencia → servicio del catálogo |

## Decisiones pendientes
- [ ] Gateway: Django + DRF o FastAPI.
- [ ] Hardware del nodo (GPU y VRAM disponibles) para elegir el tamaño de los modelos.
- [ ] Tecnología del frontend web.
