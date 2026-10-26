"""Entrena California Housing con las ocho variables de la plantilla P2."""
from pathlib import Path
import hashlib
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent

def main():
    dataset = ROOT / 'datos/california_housing.csv'
    if dataset.exists():
        frame = pd.read_csv(dataset)
    else:
        frame = fetch_california_housing(as_frame=True).frame
        dataset.parent.mkdir(exist_ok=True)
        frame.to_csv(dataset, index=False)
    X, y = frame.drop(columns='MedHouseVal'), frame['MedHouseVal']
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=.2, random_state=42)
    model = RandomForestRegressor(n_estimators=60, max_depth=16, min_samples_leaf=2,
                                  random_state=42, n_jobs=1)
    model.fit(Xtrain, ytrain)
    predictions = model.predict(Xtest)
    path = ROOT / 'modelo_california.pkl'
    joblib.dump(model, path, compress=3)
    np.testing.assert_allclose(predictions, joblib.load(path).predict(Xtest))
    metrics = {'mae_cientos_miles_usd': mean_absolute_error(ytest, predictions),
               'filas_entrenamiento': len(Xtrain), 'filas_prueba': len(Xtest),
               'variables': X.columns.tolist(), 'unidad': '100000 USD',
               'sha256_modelo': hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT / 'metricas_entrenamiento.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    main()
