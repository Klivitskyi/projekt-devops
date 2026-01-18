# Instrukcja konfiguracji CI/CD

## Wymagane Secrets w GitHub

Aby pipeline działał poprawnie, musisz skonfigurować następujące secrets w ustawieniach repozytorium GitHub (`Settings` → `Secrets and variables` → `Actions`):

### 1. REGISTRY
Registry Docker, np.:
- `ghcr.io` (GitHub Container Registry)
- `docker.io` (Docker Hub)
- `registry.example.com` (własny registry)

### 2. REMOTE_REPOSITORY
Nazwa repozytorium obrazów Docker, np.:
- `username/repo-name`
- `organization/repo-name`

### 3. DOCKER_USERNAME
Nazwa użytkownika do logowania do registry Docker

### 4. DOCKER_PASSWORD
Hasło/token do logowania do registry Docker

## Przykładowa konfiguracja dla GitHub Container Registry

1. **REGISTRY**: `ghcr.io`
2. **REMOTE_REPOSITORY**: `username/repo-name` (lub użyj `${{ github.repository }}`)
3. **DOCKER_USERNAME**: Twój username GitHub
4. **DOCKER_PASSWORD**: Personal Access Token (PAT) z uprawnieniami `write:packages`

## Jak utworzyć Personal Access Token (PAT)

1. Przejdź do: `GitHub` → `Settings` → `Developer settings` → `Personal access tokens` → `Tokens (classic)`
2. Kliknij `Generate new token (classic)`
3. Nadaj nazwę tokenowi
4. Wybierz scope: `write:packages`
5. Wygeneruj i skopiuj token
6. Dodaj jako secret `DOCKER_PASSWORD`

## Struktura branchy i tagów

- **Branch `dev`**: Automatyczny build i deploy do środowiska dev
  - Tag obrazu: `dev-<SHA7>`
  - Repliki: 1
  
- **Tagi (np. `v1.0.0`)**: Build i deploy do środowiska produkcyjnego
  - Tag obrazu: `<tag-name>`
  - Repliki: 3

## Testowanie pipeline

1. Push do brancha `dev` → uruchomi build i aktualizację manifestów dev
2. Utworzenie tagu (np. `git tag v1.0.0 && git push origin v1.0.0`) → uruchomi build i aktualizację manifestów prod

## Struktura manifestów

```
manifests/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── patch-deployment.yaml  # Aktualizowany przez CI/CD
    │   └── kustomization.yaml
    └── prod/
        ├── patch-deployment.yaml  # Aktualizowany przez CI/CD
        └── kustomization.yaml
```

Pipeline automatycznie aktualizuje plik `patch-deployment.yaml` w odpowiednim overlay z nowym tagiem obrazu.

