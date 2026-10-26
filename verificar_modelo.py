"""Comprueba el modelo real y la descarga; no genera evidencias de Render."""
import json
import math
from pathlib import Path
import tempfile

import joblib
import pandas as pd

from app import FIELDS, app, ensure_model


def main():
    sample = json.loads(Path('ejemplo_peticion.json').read_text(encoding='utf-8'))
    client = app.test_client()
    health = client.get('/')
    assert health.status_code == 200 and health.json['model_loaded'] is True
    prediction = client.post('/predict', json=sample)
    assert prediction.status_code == 200, prediction.get_data(as_text=True)
    values = prediction.json['predictions']
    assert len(values) == 1 and math.isfinite(values[0])
    assert client.post('/predict', json={}).status_code == 400
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'modelo_california.pkl'
        ensure_model(path)
        downloaded = joblib.load(path)
        expected = downloaded.predict(pd.DataFrame([sample], columns=FIELDS))[0]
        assert math.isclose(values[0], float(expected), rel_tol=1e-9)
    print('Modelo real, API y descarga desde GitHub: correctos.')
    print(json.dumps(prediction.json, ensure_ascii=False))


if __name__ == '__main__':
    main()
