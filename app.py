"""API de California Housing: Carlos Casal P2."""
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
import hashlib
import math
import os
import re
import tempfile

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge, UnsupportedMediaType

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / 'modelo_california.pkl'
MODEL_SHA256 = '73adae86829d62848e2b7ab4d4ea5ddd3aca37209969fe0a220dbecd9d010b71'
NUMERIC = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
           'total_bedrooms', 'population', 'households', 'median_income']
FIELDS = NUMERIC + ['ocean_proximity']
CATEGORIES = {'<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'}


def ensure_model(path=MODEL_PATH, repository=None, ref=None):
    """Descarga desde GitHub si falta; valida SHA-256 antes de deserializar."""
    path = Path(path)
    if not path.is_file():
        repository = repository or os.environ.get('GITHUB_REPOSITORY', '')
        ref = ref or os.environ.get('MODEL_REF', 'main')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
            raise RuntimeError('Configura GITHUB_REPOSITORY con propietario/repositorio.')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', ref):
            raise RuntimeError('MODEL_REF debe ser una rama o un commit válido.')
        url = f'https://raw.githubusercontent.com/{repository}/{ref}/modelo_california.pkl'
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with urlopen(url, timeout=60) as response:
                if urlparse(response.geturl()).hostname != 'raw.githubusercontent.com':
                    raise RuntimeError('Origen de descarga inesperado.')
                with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
                    temporary = Path(output.name)
                    digest = hashlib.sha256()
                    total = 0
                    while chunk := response.read(1024 * 1024):
                        total += len(chunk)
                        if total > 30 * 1024 * 1024:
                            raise RuntimeError('El modelo supera el tamaño permitido.')
                        digest.update(chunk)
                        output.write(chunk)
            if digest.hexdigest() != MODEL_SHA256:
                raise RuntimeError('El SHA-256 del modelo descargado no coincide.')
            os.replace(temporary, path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    if hashlib.sha256(path.read_bytes()).hexdigest() != MODEL_SHA256:
        raise RuntimeError('El fichero del modelo no coincide con el artefacto esperado.')
    return path


def validate_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError('Se espera un objeto JSON o {"instances": [...]} .')
    if 'instances' in payload:
        if set(payload) != {'instances'}:
            raise ValueError('No añadas campos junto a instances.')
        rows = payload['instances']
    else:
        rows = [payload]
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError('instances debe contener entre 1 y 100 registros.')
    for row in rows:
        if not isinstance(row, dict) or set(row) != set(FIELDS):
            raise ValueError('Cada registro debe contener exactamente: ' + ', '.join(FIELDS))
        for name in NUMERIC:
            value = row[name]
            if value is None and name == 'total_bedrooms':
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f'{name} debe ser un número finito.')
        if not isinstance(row['ocean_proximity'], str) or row['ocean_proximity'] not in CATEGORIES:
            raise ValueError('ocean_proximity debe ser una categoría conocida del dataset.')
    return rows


def create_app(model=None):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 64 * 1024
    if model is None:
        model = joblib.load(ensure_model())
        model.named_steps['modelo'].n_jobs = 1

    @app.get('/')
    def health():
        return jsonify(status='ok', model_loaded=True, author='Carlos Casal P2',
                       model='Random Forest', target='median_house_value', unit='USD')

    @app.post('/predict')
    def predict():
        try:
            rows = validate_payload(request.get_json())
        except (BadRequest, UnsupportedMediaType, ValueError) as error:
            message = str(error) if isinstance(error, ValueError) else 'Envía JSON válido con Content-Type: application/json.'
            return jsonify(error=message, author='Carlos Casal P2'), 400
        frame = pd.DataFrame(rows, columns=FIELDS)
        for field in NUMERIC:
            frame[field] = pd.to_numeric(frame[field]).astype(float)
        try:
            predictions = model.predict(frame)
            if not all(math.isfinite(float(value)) for value in predictions):
                raise ValueError('Predicción no finita.')
        except Exception:
            app.logger.exception('Error al predecir')
            return jsonify(error='No se pudo realizar la predicción.'), 500
        return jsonify(predictions=[float(value) for value in predictions], unit='USD',
                       target='median_house_value', author='Carlos Casal P2')

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(error):
        return jsonify(error='La petición supera 64 KiB.'), 413

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '5000')), debug=False)
