# 002 — Plan

> Cómo se implementa.

## Enfoque técnico
- Workflow `.github/workflows/ci.yml` con matriz por servicio.
- Pasos: `docker build` → `trivy image` → `syft` → push a GHCR → `cosign sign` (keyless con OIDC de GitHub o con par de llaves) → commit del nuevo tag en `values.yaml`.
- Argo CD instalado en k3s con una `Application` apuntando a `codigo/helm/barberforge/`.
- Kyverno con una `ClusterPolicy` de tipo `verifyImages`.

## Componentes
- `.github/workflows/`
- `codigo/helm/barberforge/values.yaml`
- Manifiestos de Argo CD y Kyverno
