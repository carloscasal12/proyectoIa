"""Reproduce el modelo de P1. Carlos Casal P2."""
from pathlib import Path
import hashlib
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / 'datos/housing.csv')
    X, y = df.drop(columns='median_house_value'), df['median_house_value']
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=.2, random_state=42)
    preprocessing = ColumnTransformer([
        ('numericas', Pipeline([('imputar', SimpleImputer(strategy='median')),
                               ('escalar', StandardScaler())]),
         X.select_dtypes(include=np.number).columns.tolist()),
        ('categoricas', Pipeline([('imputar', SimpleImputer(strategy='most_frequent')),
                                 ('codificar', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]),
         X.select_dtypes(exclude=np.number).columns.tolist())])
    model = Pipeline([('preprocesar', preprocessing), ('modelo', RandomForestRegressor(
        n_estimators=100, max_depth=18, min_samples_leaf=2, n_jobs=1, random_state=42))])
    model.fit(Xtrain, ytrain)
    predictions = model.predict(Xtest)
    mae = mean_absolute_error(ytest, predictions)
    path = ROOT / 'modelo_california.pkl'
    joblib.dump(model, path, compress=3)
    np.testing.assert_allclose(predictions, joblib.load(path).predict(Xtest))
    result = {'mae_prueba_usd': mae, 'filas_entrenamiento': len(Xtrain),
              'filas_prueba': len(Xtest), 'semilla': 42,
              'sha256_modelo': hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT / 'metricas_entrenamiento.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Carlos Casal P2\n' + json.dumps(result, indent=2))
    print('Si se sustituye el modelo entregado, actualizar MODEL_SHA256 en app.py con el hash anterior.')


if __name__ == '__main__':
    main()
