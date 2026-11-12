# Aplicación Streamlit para el precio de casas en California

La aplicación estima el precio medio de las viviendas de una zona de California.
Está formada por una API FastAPI y una interfaz Streamlit.
El usuario introduce el ingreso medio y el número medio de habitaciones.
Streamlit completa las otras seis variables con los valores de la plantilla.
Antes de enviar los datos comprueba que no faltan campos ni contienen None.
Envía los datos en JSON mediante una petición POST al endpoint /predict.
FastAPI devuelve MedHouseVal en cientos de miles de dólares.
Streamlit multiplica el resultado por 100000 y muestra el precio en dólares.
Los errores de conexión y de la API se muestran con mensajes claros.

Autores: Carlos Casal; Jorge del Hoyo Ballestin.

## Servicios desplegados en Render

| Servicio | Qué es | URL |
|----------|--------|-----|
| API existente de P2 | FastAPI usada en las pruebas reales | https://california-housing-carlos-casal-p2.onrender.com |
| API nueva de P3 | app.py y modelo adjuntos sin modificar | Pendiente de desplegar y verificar |
| Interfaz | Streamlit de la plantilla completada | Pendiente de desplegar y verificar |

La API pública de P2 utiliza un modelo diferente del adjunto a P3. Las pruebas remotas acreditan la conexión, no la ejecución del modelo adjunto. No se ha inventado una URL pública de Streamlit.

## Cómo ejecutarla en local

Desde la carpeta recursos/ejercicio_5/codigo, con Python 3.14 y el modelo adjunto en esa misma carpeta:

```powershell
python -m pip install -r requirements.txt -c constraints.txt
python -m uvicorn app:app --reload
```

En otra terminal, también desde la carpeta codigo:

```powershell
python -m streamlit run streamlit_app.py
```

Abre http://localhost:8501. Para utilizar la API local escribe http://localhost:8000 en la barra lateral, sin añadir /predict. Documentación interactiva: http://localhost:8000/docs. Por defecto, la interfaz utiliza la URL pública existente de P2.

## Despliegue en Render

Publica el contenido de codigo como raíz del repositorio, incluyendo el modelo. Si conservas toda la entrega en el repositorio, configura recursos/ejercicio_5/codigo como Root Directory para ambos servicios.

| Servicio | Build Command | Start Command |
|---|---|---|
| API | pip install -r requirements.txt -c constraints.txt | uvicorn app:app --host 0.0.0.0 --port $PORT |
| Streamlit | pip install -r requirements.txt -c constraints.txt | streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true |

Estos comandos están preparados para Render; el despliegue de P3 todavía no está verificado. render.yaml configura dos Web Services en plan free. Antes de desplegar la interfaz, cambia la constante API_URL de streamlit_app.py por la URL que Render asigne a la API de P3. La URL puede cambiarse temporalmente en la barra lateral. Esta plantilla usa una constante, no una variable de entorno.

Referencia oficial del Blueprint: https://render.com/docs/blueprint-spec

## Documentación de la API

URL base comprobada: https://california-housing-carlos-casal-p2.onrender.com

### `POST /predict`

Recibe las ocho variables numéricas de una zona censal en un cuerpo JSON. Devuelve MedHouseVal, el precio medio de la vivienda en unidades de 100000 USD.

**Ejemplo de petición**

```json
{
  "MedInc": 3.5,
  "HouseAge": 29.0,
  "AveRooms": 5.2,
  "AveBedrms": 1.05,
  "Population": 1166.0,
  "AveOccup": 2.8,
  "Latitude": 34.26,
  "Longitude": -118.49
}
```

**Ejemplo de respuesta correcta (200)**

```json
{"MedHouseVal": 2.1377044932162446}
```

Respuesta real obtenida de la API pública de P2. La interfaz muestra **$213,770**, redondeado a dólares enteros como pide la plantilla, y el valor original en un texto explicativo. El modelo adjunto a P3 puede devolver otro resultado.

MedInc se expresa en decenas de miles de dólares (3.5 equivale a 35000 USD); HouseAge en años; AveRooms y AveBedrms son medias por hogar; Population es la población; AveOccup es la ocupación media; Latitude y Longitude son coordenadas en grados. Los seis valores por defecto se conservan como en la plantilla.

**Errores**

| Código | Cuándo ocurre | Qué muestra la aplicación |
|--------|---------------|---------------------------|
| 422 | Falta un campo o tiene un tipo incorrecto | Un mensaje con HTTP 422 y el detalle de response.text |
| 500 u otro código distinto de 200 | Fallo de la API | Un único mensaje con el código HTTP y el texto de respuesta, aunque no sea JSON |
| Sin respuesta | La API no está disponible o tarda demasiado | Pide revisar la URL y el estado del servicio, esperar al arranque y reintentar |

Si se omite HouseAge, la validación local muestra «Faltan variables obligatorias: HouseAge» y no envía la petición. Activando además «saltar la validación local», se envía el JSON incompleto para provocar el 422 real de la API. TIMEOUT se conserva en 90 segundos.

## Pruebas reproducibles

Desde la raíz de la carpeta dawm2d_opia_p3:

```powershell
python -m pip install -r recursos/ejercicio_5/codigo/requirements.txt -c recursos/ejercicio_5/codigo/constraints.txt
python recursos/ejercicio_5/herramientas/pruebas_plantilla.py
```

Las pruebas ejecutan la interfaz con Streamlit AppTest. Cubren None y campos ausentes, 0.0 válido, conversión de 4.53 a $453,000, bloqueo local sin POST, 422 real al saltar la validación, predicción real de P2, URL errónea real, error 500 de texto y timeout simulados. Los resultados originales están en recursos/ejercicio_2/resultados_pruebas.json. Al repetirlas, se guardan en recursos/ejercicio_5/resultados_repeticion.json.

Las capturas nuevas incluyen los autores y P3. La memoria distingue Streamlit local, API pública existente y despliegue pendiente de P3.
