# 001 — API de citas en Kubernetes

> Qué hace esta feature y criterios de aceptación.

## Descripción
Base del proyecto: estructura del repositorio, API Gateway con la gestión de citas y catálogo de servicios, y base de datos PostgreSQL, todo desplegado en k3s mediante un Helm chart.

## Historias de usuario
- Como cliente, quiero ver los servicios con precio y duración para elegir uno.
- Como cliente, quiero consultar los horarios disponibles de un barbero y agendar una cita.
- Como barbero, quiero ver y cancelar las citas de mi agenda.

## Criterios de aceptación
- [ ] Existen endpoints REST para barberos, servicios y citas (crear, listar, cancelar).
- [ ] Existe un endpoint de disponibilidad que devuelve huecos libres según la duración del servicio.
- [ ] No es posible agendar dos citas que se solapen para el mismo barbero.
- [ ] PostgreSQL corre con la extensión pgvector habilitada.
- [ ] `helm install` despliega API, PostgreSQL y Redis en k3s y la API responde un health check.
- [ ] Los secretos (credenciales de BD) se inyectan como Secret de Kubernetes, no en el código.
