# Tech Stack

> Tecnologías y convenciones.

## Microservicios
| Servicio | Tecnología | Responsabilidad |
|---|---|---|
| API Gateway | Django + Django REST Framework (alternativa: FastAPI) | Citas, catálogo, autenticación, entrada del chat web |
| Servicio de IA | Python + Ollama | RAG, tool calling y modelo de visión |
| Bot de WhatsApp | Node.js + whatsapp-web.js / Baileys | Canal de WhatsApp (número de prueba) |
| Frontend web | Por definir | Chat y agendamiento para el cliente |

## Datos
- **PostgreSQL + pgvector:** una sola base de datos para las citas y para los embeddings del RAG.
- **Redis:** cola de trabajos para las tareas lentas de IA (análisis de imágenes), procesadas por un worker.

## IA local (Ollama)
- **Modelo de texto:** Llama 3.2 3B o Qwen 2.5 3B.
- **Embeddings:** `nomic-embed-text`.
- **Visión:** `qwen2.5vl:3b` o `moondream`.
- **Regla:** el RAG contiene solo información estática (precios, servicios, productos). La disponibilidad de citas se consulta con *tool calling*, por ejemplo `consultar_disponibilidad()` y `agendar_cita()`.

## Infraestructura
- **Clúster:** k3s (alternativa: kind).
- **Empaquetado:** Helm chart.
- **GitOps:** Argo CD sincroniza el clúster con el repositorio.
- **Políticas (extra):** Kyverno verifica la firma de las imágenes antes de ejecutarlas.

## CI/CD (GitHub Actions)
`build → Trivy → SBOM con Syft → firma con Cosign → push a GHCR → actualización de values.yaml del Helm chart`

## Observabilidad
- **OpenTelemetry Collector** → Prometheus (métricas), Tempo (trazas), Loki (logs).
- **Grafana:** consultas atendidas por el bot, latencia del modelo, tamaño de la cola de Redis, CPU y memoria del nodo.
- Si hay GPU NVIDIA: exportador DCGM para medir la VRAM.

## Convenciones
- Código en la carpeta [`codigo/`](../../codigo/), un subdirectorio por microservicio.
- Una imagen de contenedor por servicio, con su propio `Dockerfile`.
- Configuración y secretos por variables de entorno; los secretos nunca se versionan.
- Cada feature se documenta en `spec/features/NNN-nombre/` (spec → plan → tasks) antes de implementarse.
- Privacidad: las imágenes de los clientes no se persisten; se borran apenas termina su procesamiento.
