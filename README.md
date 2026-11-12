# Precio de casas en California — P3

Autores: Carlos Casal; Jorge del Hoyo Ballestin.

## Servicios reales en Render

Verificados el 12/11/2026 en plan gratuito, región Oregon y Python 3.14.5.

| Servicio | URL |
|---|---|
| FastAPI P3 | https://california-carlos-p3-api.onrender.com |
| Documentación interactiva | https://california-carlos-p3-api.onrender.com/docs |
| Streamlit P3 | https://california-carlos-p3-web.onrender.com |

Repositorio: https://github.com/carloscasal12/proyectoIa/tree/p3-render
El código de esta carpeta se publica en la raíz de esa rama. Ambos servicios usan el modelo adjunto de P3.

## Ejecución y despliegue

Desde esta carpeta, instalar con Python 3.14.5: 

pip install -r requirements.txt -c constraints.txt

API: uvicorn app:app --host 0.0.0.0 --port $PORT

Web: streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true

En local sustituir $PORT por 8000 para la API y 8501 para Streamlit. La barra lateral permite elegir http://localhost:8000.
API_URL apunta por defecto a la API pública de P3. TIMEOUT=90 segundos. Los servicios gratuitos pueden tardar en arrancar tras inactividad.
render.yaml describe ambos servicios. Al usar toda la entrega como repositorio, configurar dawm2d_opia_p3/recursos/ejercicio_5/codigo como Root Directory; si se publica esta carpeta como raíz, dejar Root Directory vacío.

## Contrato POST /predict

Enviar JSON con las ocho variables numéricas:

```json
{"MedInc":3.5,"HouseAge":29.0,"AveRooms":5.2,"AveBedrms":1.05,"Population":1166.0,"AveOccup":2.8,"Latitude":34.26,"Longitude":-118.49}
```

Respuesta real de P3 (HTTP 200):

```json
{"MedHouseVal":1.5126018234536092}
```

MedHouseVal está en cientos de miles de dólares. La interfaz multiplica por 100000 y muestra **$151,260**, conservando el valor original debajo.
MedInc se expresa en decenas de miles de dólares; HouseAge en años; AveRooms y AveBedrms son medias por hogar; Population es la población; AveOccup la ocupación media y Latitude/Longitude coordenadas en grados.

El usuario introduce MedInc y AveRooms. Las demás variables conservan los valores de la plantilla. find_missing detecta campos ausentes o None y admite 0.0.

| Error | Comportamiento |
|---|---|
| Campo ausente | Validación local: indica HouseAge y no hace POST |
| HTTP 422 | Al saltar la validación, muestra el código y response.text |
| HTTP 500 u otro | Muestra el código y response.text, aunque no sea JSON |
| Fallo de conexión o timeout | Pide revisar URL, estado del servicio y reintentar |

## Evidencias y comprobaciones

En ../.. (recursos): ejercicio_1/comprobaciones_http.json contiene respuestas HTTP reales de health, predicción y error 422. render_api.log y render_streamlit.log son exportaciones reales de Render con marcas UTC; los JSON conservan identificadores y etiquetas originales. render_*_deploy.json acredita estado live y commit.
Las capturas de los ejercicios 1 a 5 proceden de las páginas públicas en Render, obtenidas con capturas_render.cjs, sin alterar la página. Los logs streamlit_stdout/stderr anteriores son locales y se conservan identificados.

Desde la raíz de dawm2d_opia_p3:

```powershell
python recursos/ejercicio_5/herramientas/pruebas_plantilla.py
python recursos/ejercicio_5/herramientas/generar_documentos.py
python recursos/ejercicio_5/herramientas/verificar_entrega.py
```

AppTest comprueba funciones, validación local, predicción y 422 de la API real de P3, URL incorrecta real y errores 500/timeout simulados. Sus resultados se guardan en resultados_repeticion.json. Las capturas del navegador acreditan además la interfaz desplegada. Las herramientas documentales usan requirements-herramientas.txt.
