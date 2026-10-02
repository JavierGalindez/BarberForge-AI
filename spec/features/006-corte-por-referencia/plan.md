# 006 — Plan

Cómo se implementa.

## Enfoque técnico

* El backend en FastAPI recibe la imagen, verifica el consentimiento y encola un trabajo en Redis; devuelve un ID de trabajo.
* Un worker en `codigo/ia/worker/` toma el trabajo, llama al modelo de visión en Ollama, borra la imagen y guarda solo el texto resultante.
* La descripción se usa como consulta al RAG para encontrar el servicio del catálogo.
* El cliente consulta el estado del trabajo (polling) o recibe la respuesta por el canal de chat.

## Componentes

* `codigo/backend/` (endpoint de subida y consentimiento)
* `codigo/ia/worker/`
* `codigo/frontend/` y `codigo/whatsapp-bot/` (envío de imágenes)
