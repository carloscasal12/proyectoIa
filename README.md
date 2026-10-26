# California Housing API — Carlos Casal P2
1. Se creó la cuenta de Render y se autorizó la conexión con GitHub.
2. Repositorio público: https://github.com/carloscasal12/proyectoIa
3. Se subieron entrenamiento, modelo, dataset, API y dependencias a la rama main.
4. El entrenamiento reproducible está en entrenar_modelo.py y usa datos/housing.csv.
5. Se creó un Blueprint en Render a partir de render.yaml.
6. Se configuró Python 3.14.5 y una instancia Free.
7. Construcción: `pip install -r requirements.txt`.
8. Inicio: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120`.
9. Variables: GITHUB_REPOSITORY=carloscasal12/proyectoIa y MODEL_REF=main.
10. El servicio alcanzó el estado Live y publicó una URL HTTPS.
11. URL final: https://california-housing-carlos-casal-p2.onrender.com
12. GET / comprueba el estado y confirma que el modelo está cargado.
13. POST /predict recibe el JSON de ejemplo_peticion.json y devuelve una predicción en USD.
14. Se ejecutó medir_tiempos.py contra Render: cinco peticiones HTTP 200 con respuesta válida.
15. Se verificó la descarga real del modelo desde GitHub con destino inicialmente inexistente.
16. La descarga valida SHA-256 antes de cargar el modelo mediante joblib.
17. Las predicciones describen zonas censales; los datos históricos pueden introducir sesgos.
