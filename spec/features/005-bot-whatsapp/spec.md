# 005 — Bot de WhatsApp

> Qué hace esta feature y criterios de aceptación.

## Descripción
Microservicio en Node.js que conecta WhatsApp con el asistente, para que el cliente tenga la misma experiencia que en el chat web.

## Criterios de aceptación
- [ ] El bot recibe mensajes de WhatsApp y los reenvía al servicio de IA.
- [ ] Las respuestas del asistente (precios, disponibilidad, confirmación de cita) llegan al cliente por WhatsApp.
- [ ] Se usa **un número de prueba**, nunca el número real de la barbería.
- [ ] La sesión de WhatsApp persiste en un volumen para no reescanear el QR en cada reinicio.
- [ ] La limitación de usar una librería no oficial queda documentada.
