# Predicción del precio de casas en California (servicio web)
Autores: Carlos Casal; segundo integrante pendiente de identificar.
## Contenido del repositorio
FastAPI app.py, modelo_california.pkl, entrenar_modelo.py, requirements.txt y medir_tiempos.py.
El modelo utiliza las ocho variables de la plantilla y predice MedHouseVal en unidades de 100000 USD.
Datos reproducibles: datos/california_housing.csv, obtenidos mediante fetch_california_housing.
## Pasos del despliegue
1. Se creó la cuenta de Render y se autorizó el acceso al repositorio de GitHub.
2. Se publicó el proyecto en https://github.com/carloscasal12/proyectoIa, rama main.
3. Se entrenó y comprobó el modelo en Linux; entrenamiento reproducible: `python entrenar_modelo.py`.
4. Se creó el Blueprint de Render con render.yaml, Python 3.14.5 e instancia Free.
5. Build Command: `pip install -r requirements.txt`.
6. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`.
7. Se comprobaron GET / y POST /predict usando el JSON de ejemplo_peticion.json.
8. Se ejecutó la plantilla medir_tiempos.py y se conservaron los tiempos y respuestas reales.
9. Al faltar el modelo local, load_model lo descarga desde la URL raw de GitHub.
## URL final
https://california-housing-carlos-casal-p2.onrender.com
