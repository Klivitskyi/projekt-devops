"""
Główna aplikacja Flask - przykładowa aplikacja webowa
"""
from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfiguracja z zmiennych środowiskowych
VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(ENVIRONMENT == 'development'))

