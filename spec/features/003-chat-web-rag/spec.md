# 003 — Chat web con RAG y tool calling

> Qué hace esta feature y criterios de aceptación.

## Descripción
Asistente conversacional en la web. Responde sobre precios, servicios y productos usando RAG sobre la base de conocimiento de la barbería, y consulta disponibilidad y agenda citas en tiempo real mediante tool calling contra la API.

## Historias de usuario
- Como cliente, quiero preguntar cuánto cuesta un corte con barba y recibir el precio correcto.
- Como cliente, quiero pedir una cita para mañana en la tarde y que el asistente me ofrezca horarios reales y la agende.

## Criterios de aceptación
- [ ] Los documentos de la barbería (catálogo, precios, productos) se indexan con `nomic-embed-text` en pgvector.
- [ ] Las respuestas sobre precios y servicios usan información de la base de conocimiento.
- [ ] La disponibilidad **nunca** sale del RAG: el modelo llama a `consultar_disponibilidad()`.
- [ ] El modelo puede crear una cita con `agendar_cita()` tras la confirmación del cliente.
- [ ] Si la pregunta está fuera del dominio de la barbería, el asistente lo indica en lugar de inventar.
- [ ] Todo se ejecuta con Ollama local, sin APIs externas.
