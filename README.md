# BarberForge AI

Plataforma de código abierto para barberías que combina inteligencia artificial local e infraestructura en la nube moderna para atender clientes, gestionar citas y recomendar servicios.

Proyecto del diplomado.

## Funcionalidades

- **Atención por WhatsApp y web:** el cliente conversa desde la aplicación web o por WhatsApp.
- **Asistente inteligente (RAG local):** responde sobre precios, servicios y productos con Ollama. La disponibilidad se consulta en tiempo real en la base de datos mediante *tool calling*.
- **Corte por referencia (IA multimodal):** el cliente envía la foto de un corte y el sistema identifica el estilo, le asigna un servicio del catálogo, informa precio y duración y ofrece agendar.

## Stack

| Área | Tecnologías |
|---|---|
| Servicios | API Gateway (Django + DRF), servicio de IA (Python), bot de WhatsApp (Node.js) |
| Datos | PostgreSQL + pgvector, Redis (cola de trabajos) |
| IA local | Ollama: modelo de texto 3B, `nomic-embed-text` y modelo de visión |
| Infraestructura | Kubernetes (k3s) + Helm |
| DevSecOps / GitOps | GitHub Actions, Trivy, Syft (SBOM), Cosign, GHCR, Argo CD |
| Observabilidad | OpenTelemetry, Prometheus, Tempo, Loki, Grafana |

## Estructura del repositorio

```
BarberForge-AI/
├── spec/
│   ├── constitution/   # misión, tech stack y roadmap
│   └── features/       # spec, plan y tareas de cada feature
└── codigo/             # código fuente de los servicios
```

El desarrollo sigue el enfoque *spec-driven*: cada feature se documenta en `spec/features/` antes de implementarse. El orden de las fases está en el [roadmap](spec/constitution/roadmap.md).

## Privacidad

Todo se procesa localmente, sin APIs externas. Las imágenes se reciben solo con consentimiento explícito y se eliminan apenas se procesan (Ley 1581 de 2012).

## Limitaciones

El bot de WhatsApp usa una librería no oficial y funciona únicamente con un número de prueba. Si ese número se bloquea, el plan B es un bot de Telegram.
