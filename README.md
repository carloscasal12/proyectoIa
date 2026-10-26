# California Housing API — Carlos Casal P2 — segundo integrante pendiente
1. Crear una cuenta personal de GitHub y una cuenta de Render.
2. Reunir los archivos de ejercicios 2-6 en la raíz del repositorio público, conservando datos/housing.csv; subirlos a GitHub.
3. El código de entrenamiento está en entrenar_modelo.py; el modelo conserva el Pipeline de P1.
4. En Render, crear un Web Service y conectar ese repositorio y su rama main.
5. Seleccionar Python y la instancia Free; fijar PYTHON_VERSION=3.14.5.
6. Comando de construcción: `pip install -r requirements.txt`.
7. Comando de inicio: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120`.
8. Configurar GITHUB_REPOSITORY=carloscasal12/proyectoIa y MODEL_REF=main o el commit del modelo.
9. La descarga desde GitHub solo se realiza si falta el modelo local y valida su SHA-256.
10. Esperar a que Render confirme el despliegue y verificar `GET /`.
11. Enviar ejemplo_peticion.json a `POST /predict` con Content-Type: application/json.
12. Ejecutar `python medir_tiempos.py URL_REAL_RENDER` para guardar cinco mediciones reales.
13. Capturar repositorio, conexión, configuración, health-check y predicción con «Carlos Casal P2».
14. URL final: PENDIENTE DE DESPLIEGUE REAL EN RENDER.
15. Repositorio público: https://github.com/carloscasal12/proyectoIa (pendiente de subir los archivos).
16. El servicio estima el valor mediano por zona censal en USD; no tasa viviendas individuales.
17. Los datos históricos y los sesgos geográficos limitan el uso de las predicciones.
