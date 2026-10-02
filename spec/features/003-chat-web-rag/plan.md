# 003 — Plan

Cómo se implementa.

## Enfoque técnico

* Servicio de IA en `codigo/ia/` (Python) que expone un endpoint `/chat`.
* Ollama desplegado en el clúster con el modelo de texto (Llama 3.2 3B o Qwen 2.5 3B) y `nomic-embed-text`.
* Ingesta: script que divide los documentos en fragmentos, genera embeddings y los guarda en una tabla pgvector.
* Herramientas expuestas al modelo: `consultar_disponibilidad(servicio, fecha, barbero)` y `agendar_cita(...)`, que llaman a la API del backend.
* Frontend web desarrollado en **React + Vite** (`codigo/frontend/`) con interfaz de ventana de chat.

## Componentes

* `codigo/ia/`
* `codigo/frontend/`
* Base de conocimiento en `codigo/ia/conocimiento/`
