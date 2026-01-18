.PHONY: help install test lint format build run clean docker-build docker-run

help:
	@echo "Dostępne komendy:"
	@echo "  make install     - Instalacja zależności"
	@echo "  make test        - Uruchomienie testów"
	@echo "  make lint        - Sprawdzenie kodu (flake8)"
	@echo "  make format      - Formatowanie kodu"
	@echo "  make build       - Budowanie aplikacji"
	@echo "  make run         - Uruchomienie aplikacji lokalnie"
	@echo "  make docker-build - Budowanie obrazu Docker"
	@echo "  make docker-run  - Uruchomienie kontenera Docker"
	@echo "  make clean       - Usunięcie plików tymczasowych"
	@echo "  make generate-manifests - Generowanie manifestów ArgoCD"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/ scripts/

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

build:
	python -m py_compile src/*.py

run:
	export FLASK_APP=src.app && flask run --host=0.0.0.0 --port=5000

docker-build:
	docker build -t devops-app:latest .

docker-run:
	docker run -p 5000:5000 -e ENVIRONMENT=development devops-app:latest

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

generate-manifests:
	python scripts/generate-manifests.py

