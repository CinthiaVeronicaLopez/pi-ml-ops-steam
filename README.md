# pi-ml-ops-steam
<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

¡Bienvenidos al primer proyecto individual de la etapa de labs! En esta ocasión, deberán hacer un trabajo situándose en el rol de un ***MLOps Engineer***.  

<hr>  

## **Descripción del problema (Contexto y rol a desarrollar)**

## Contexto

Tienes tu modelo de recomendación dando unas buenas métricas 😏, y ahora, cómo lo llevas al mundo real? 👀

El ciclo de vida de un proyecto de Machine Learning debe contemplar desde el tratamiento y recolección de los datos (Data Engineer stuff) hasta el entrenamiento y mantenimiento del modelo de ML según llegan nuevos datos.


## Rol a desarrollar

Empezaste a trabajar como Data Scientist en Steam, una plataforma multinacional de videojuegos. El mundo es bello y vas a crear tu primer modelo de ML que soluciona un problema de negocio: Steam pide que te encargues de crear un sistema de recomendación de videojuegos para usuarios. 😟

Vas a sus datos y te das cuenta que la madurez de los mismos es poca (ok, es nula 😭 ): Datos anidados, de tipo raw, no hay procesos automatizados para la actualización de nuevos productos, entre otras cosas… haciendo tu trabajo imposible 😩 .

Debes empezar desde 0, haciendo un trabajo rápido de Data Engineer y tener un MVP (Minimum Viable Product) para el cierre del proyecto! Tu cabeza va a explotar 🤯, pero al menos sabes cual es, conceptualmente, el camino que debes de seguir ❗. Así que espantas los miedos y pones manos a la obra 💪

<p align="center">
<img src="https://github.com/HX-PRomero/PI_ML_OPS/raw/main/src/DiagramaConceptualDelFlujoDeProcesos.png"  height=500>
</p>

<sub> Nota que aquí se reflejan procesos, no herramientas tecnológicas. Haz el ejercicio de entender qué herramienta del stack corresponde a cada parte del proceso<sub/>

## Transformaciones ETL
En el archivo etl.ipynb que se proporciona hay una serie de pasos que se realizó para extraer, transformar y cargar datos en un DataFrame steam.

## Análisis exploratorio de los datos EDA
Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior. Las nubes de palabras dan una buena idea de cuáles palabras son más frecuentes en los títulos, se deja capturas obtenidas del DataFrame steam y se puede explorar en el archivo eda.ipynb.

## API en desarrollo: funciones API con FastAPI
Se Propone disponibilizar los datos usando el framework FastAPI. Las consultas que se propones son las siguientes:

<sub> Debes crear las siguientes funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).<sub/>


+ def **PlayTimeGenre( *`genero` : str* )**:
    Debe devolver `año` con mas horas jugadas para dicho género.
  
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

+ def **UsersRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **UsersNotRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **sentiment_analysis( *`año` : int* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. 

Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}

<br/>

## Detalles adicionales del proyecto

Aquí encontrarás información adicional y recursos relacionados de mi proyecto:

* `Video explicativo:` Se ha creado un [video explicativo](video.mp4)  donde te muestro algunas funciones de mi proyecto con el uso de la API.

* `Acceso a la API:` En el Siguiente [enlace de la API](https://localhost:80) podras encontrar las funciones de este proyecto.

* `Acceso rápido:`
- Visualize [EDA](eda.ipynb) notebook.
- Visualize [ETL](etl.ipynb) notebook.
- Visualize [`API`](./api/main.py)

<br/>