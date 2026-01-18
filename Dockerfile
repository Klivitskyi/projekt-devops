# Multi-stage build dla optymalizacji obrazu
FROM python:3.11-slim as builder

WORKDIR /app

# Instalacja zależności
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage produkcyjny
FROM python:3.11-slim

WORKDIR /app

# Kopiowanie zależności z buildera
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY . .

# Ustawienie PATH dla lokalnych pakietów
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Port aplikacji
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

# Uruchomienie aplikacji przez gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "src.app:app"]

