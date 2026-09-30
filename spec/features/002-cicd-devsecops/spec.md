# 002 — CI/CD DevSecOps y GitOps

> Qué hace esta feature y criterios de aceptación.

## Descripción
Cada cambio en Git dispara un pipeline que construye, escanea, genera el SBOM y firma las imágenes; luego actualiza el Helm chart y Argo CD sincroniza el clúster sin intervención manual.

## Criterios de aceptación
- [ ] Un push a `main` ejecuta el pipeline en GitHub Actions.
- [ ] Trivy escanea cada imagen y el pipeline falla con vulnerabilidades CRITICAL.
- [ ] Syft genera el SBOM de cada imagen y se publica como artefacto o attestation.
- [ ] Cosign firma cada imagen publicada en GHCR.
- [ ] El pipeline actualiza el tag de la imagen en `values.yaml`.
- [ ] Argo CD detecta el cambio y despliega la nueva versión.
- [ ] (Extra) Kyverno rechaza imágenes sin firma válida.
