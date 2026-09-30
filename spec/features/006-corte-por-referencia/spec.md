# 006 — Corte por referencia (multimodal)

> Qué hace esta feature y criterios de aceptación.

## Descripción
El cliente envía la foto de un corte que vio en internet o en redes. Un modelo de visión local describe el estilo (por ejemplo, "fade bajo con textura arriba"), el RAG lo asocia a un servicio del catálogo y el asistente informa precio y duración, con opción de agendar.

## Historia de usuario
- Como cliente, quiero enviar la foto de un corte y saber qué servicio es, cuánto cuesta y cuándo puedo hacérmelo.

## Criterios de aceptación
- [ ] Antes de recibir la imagen se solicita consentimiento explícito (Ley 1581 de 2012).
- [ ] La imagen se procesa de forma asíncrona mediante la cola de Redis y un worker.
- [ ] El modelo de visión (`qwen2.5vl:3b` o `moondream`) devuelve una descripción del estilo.
- [ ] La descripción se asocia al servicio más cercano del catálogo, con precio y duración.
- [ ] El asistente ofrece agendar la cita directamente.
- [ ] La imagen se elimina apenas termina el procesamiento y nunca se guarda en la base de datos.
- [ ] Funciona desde el chat web y desde WhatsApp.
