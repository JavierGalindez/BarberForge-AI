# Misión

> Qué construimos y para quién.

## Producto
**BarberForge AI** es una plataforma de código abierto para barberías que combina inteligencia artificial local e infraestructura en la nube moderna para atender clientes, gestionar citas y recomendar servicios.

## Para quién
- **Clientes de la barbería:** consultan precios, servicios y productos, agendan citas y encuentran el corte que buscan a partir de una foto de referencia.
- **Barberos y administrador:** gestionan la agenda y el catálogo sin atender manualmente cada mensaje.
- **Contexto académico:** proyecto del diplomado. Debe cumplir la rúbrica: contenedores, orquestación, IA local, flujo multimodal, seguridad de la cadena de suministro y observabilidad.

## Qué hace
1. **Atención por WhatsApp y web.** El cliente conversa desde la aplicación web o desde el WhatsApp de la barbería (microservicio en Node.js).
2. **Asistente inteligente (RAG local).** Ollama responde sobre precios, servicios y productos consultando la base de conocimiento (catálogo y tablas de precios). La disponibilidad y el agendamiento se consultan en tiempo real en la base de datos mediante *tool calling*, nunca desde el RAG.
3. **Corte por referencia (IA multimodal).** El cliente envía la foto de un corte que le gusta. Un modelo de visión local identifica el estilo, lo relaciona con un servicio del catálogo e informa precio y duración, con opción de agendar.

## Diferenciadores
- **100 % open source:** sin licencias comerciales ni cobros por APIs externas.
- **Privacidad y soberanía de datos:** todo se procesa localmente. Se pide consentimiento explícito antes de recibir imágenes y se eliminan apenas se procesan (Ley 1581 de 2012).
- **DevSecOps y GitOps de punta a punta:** imágenes escaneadas, con SBOM y firmadas, desplegadas por Argo CD.

## Fuera de alcance
- Visagismo y análisis del rostro del cliente.
- Simulador de cortes sobre la foto del cliente (ComfyUI / inpainting).
- Pagos en línea.

## Limitaciones conocidas
- La integración con WhatsApp usa una librería no oficial (whatsapp-web.js o Baileys), que va contra los términos de WhatsApp y puede provocar el bloqueo del número. Se usa **solo un número de prueba**, nunca el real de la barbería. Plan B: bot de Telegram (API oficial y gratuita).
- Sin GPU dedicada, los modelos (texto 3B y visión pequeño) funcionan pero con mayor latencia.
