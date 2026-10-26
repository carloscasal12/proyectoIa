"""Comprueba el modelo real y la descarga; no genera evidencias de Render."""
import json
import math
from pathlib import Path
import tempfile

import joblib
import pandas as pd

from fastapi.testclient import TestClient
from app import app, download_model, load_model


def main():
    sample = json.loads(Path('ejemplo_peticion.json').read_text(encoding='utf-8'))
    with TestClient(app) as client:
        health = client.get('/')
        assert health.status_code == 200 and health.json() == {'status': 'ok'}
        prediction = client.post('/predict', json=sample)
        assert prediction.status_code == 200, prediction.text
        value = prediction.json()['MedHouseVal']
        assert math.isfinite(value)
        assert client.post('/predict', json={'MedInc': 1.0}).status_code == 422
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'modelo_california.pkl'
        downloaded = load_model(str(path))
        expected = downloaded.predict(pd.DataFrame([sample]))[0]
        assert math.isclose(value, float(expected), rel_tol=1e-9)
    print('Modelo real, API y descarga desde GitHub: correctos.')
    print(json.dumps(prediction.json(), ensure_ascii=False))


if __name__ == '__main__':
    main()
