"""
Główna aplikacja Flask - przykładowa aplikacja webowa
"""
from flask import Flask, jsonify, request
import os
import logging
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfiguracja z zmiennych środowiskowych
VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Metryki Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

APP_INFO = Gauge(
    'app_info',
    'Application information',
    ['version', 'environment']
)

# Ustawienie informacji o aplikacji
APP_INFO.labels(version=VERSION, environment=ENVIRONMENT).set(1)


@app.route('/')
def health_check():
    """Endpoint sprawdzający zdrowie aplikacji"""
    return jsonify({
        'status': 'healthy',
        'version': VERSION,
        'environment': ENVIRONMENT
    }), 200


@app.route('/api/info')
def info():
    """Endpoint zwracający informacje o aplikacji"""
    return jsonify({
        'application': 'DevOps Demo Application',
        'version': VERSION,
        'environment': ENVIRONMENT,
        'description': 'Aplikacja demonstracyjna dla projektu DevOps'
    }), 200


@app.route('/api/echo', methods=['POST'])
def echo():
    """Endpoint echo - zwraca przesłane dane"""
    data = request.get_json()
    logger.info(f"Received data: {data}")
    return jsonify({
        'received': data,
        'timestamp': str(os.popen('date').read().strip() if os.name != 'nt' else 'N/A')
    }), 200


@app.route('/metrics')
def metrics():
    """Endpoint Prometheus metrics - do scrapowania metryk"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.before_request
def before_request():
    """Middleware do zbierania metryk przed każdym requestem"""
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()


@app.after_request
def after_request(response):
    """Middleware do zbierania metryk po każdym requestem"""
    # Oblicz czas trwania requestu
    duration = time.time() - request.start_time
    
    # Zbierz metryki
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown'
    ).observe(duration)
    
    ACTIVE_REQUESTS.dec()
    
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(ENVIRONMENT == 'development'))

