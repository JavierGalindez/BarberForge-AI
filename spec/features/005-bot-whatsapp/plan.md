# 005 — Plan

> Cómo se implementa.

## Enfoque técnico
- `codigo/whatsapp-bot/` con whatsapp-web.js o Baileys.
- Cada mensaje entrante se envía al endpoint `/chat` del servicio de IA, usando el número del cliente como identificador de conversación.
- PersistentVolume para la sesión.
- Plan B: bot de Telegram con su API oficial si el número es bloqueado.

## Componentes
- `codigo/whatsapp-bot/`
- Plantilla del Helm chart para el bot
