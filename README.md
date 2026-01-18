# DevOps Project - Python Application z CI/CD dla ArgoCD

## Opis projektu

Projekt demonstracyjny prezentujący kompleksowe podejście DevOps do wytwarzania, testowania i wdrażania aplikacji Python z wykorzystaniem GitHub Actions CI/CD oraz ArgoCD do zarządzania wdrożeniami w Kubernetes.

## Struktura projektu

```
projekt-devops/
├── src/                    # Kod źródłowy aplikacji
├── tests/                  # Testy jednostkowe
├── manifests/              # Manifesty Kubernetes/ArgoCD
│   ├── base/              # Bazowe manifesty
│   └── overlays/          # Overlays dla różnych środowisk
│       ├── dev/           # Środowisko deweloperskie
│       └── prod/          # Środowisko produkcyjne
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── scripts/                # Skrypty pomocnicze
├── Dockerfile              # Obraz Docker aplikacji
├── requirements.txt        # Zależności Python
├── README.md              # Dokumentacja projektu
├── SETUP.md               # Instrukcja konfiguracji CI/CD
└── DOKUMENTACJA.md        # Pełna dokumentacja projektu
```

## Szybki start

1. Klonowanie repozytorium
2. Konfiguracja secrets w GitHub (zobacz [SETUP.md](SETUP.md))
3. Instalacja zależności: `pip install -r requirements.txt`
4. Uruchomienie testów: `pytest tests/`
5. Budowanie obrazu Docker: `docker build -t app:latest .`

## CI/CD Pipeline (GitOps)

Pipeline działa automatycznie przy:
- **Push do brancha `dev`**: Build i deploy do środowiska dev (1 replika)
- **Utworzenie tagu** (np. `v1.0.0`): Build i deploy do środowiska prod (3 repliki)
- **Pull Request**: Tylko testy i security scanning

### Etapy pipeline:

1. **Test & Security Scan**
   - Uruchomienie testów jednostkowych (pytest)
   - Skanowanie zależności (pip-audit)
   - Analiza bezpieczeństwa kodu (bandit)

2. **Build & Push Docker Image**
   - Budowanie obrazu Docker
   - Publikacja do registry (konfigurowalne przez secrets)
   - Tagowanie obrazu: `dev-<SHA7>` dla dev, `<tag-name>` dla prod

3. **Update Manifests for ArgoCD**
   - Automatyczna aktualizacja `patch-deployment.yaml` w odpowiednim overlay
   - Commit i push zmian do repozytorium (GitOps)

## Konfiguracja

Przed pierwszym użyciem należy skonfigurować secrets w GitHub:
- `REGISTRY` - Registry Docker (np. `ghcr.io`)
- `REMOTE_REPOSITORY` - Nazwa repozytorium obrazów
- `DOCKER_USERNAME` - Username do registry
- `DOCKER_PASSWORD` - Hasło/token do registry

Szczegółowe instrukcje w [SETUP.md](SETUP.md).

## Dokumentacja

- [SETUP.md](SETUP.md) - Instrukcja konfiguracji CI/CD
- [DOKUMENTACJA.md](DOKUMENTACJA.md) - Pełna dokumentacja projektu

