import pandas as pd
import numpy as np
import uvicorn
import pickle
import gzip
from enum import Enum
from fastapi import FastAPI, HTTPException
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils.extmath import randomized_svd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors

app = FastAPI()


# Raiz
@app.get("/")
def Hello():
    return "Cinthia López"


# IMPORTAMOS LOS DATOS
# data = pd.read_csv("steam.csv", encoding='utf-8')
# Importar los datos en csv comprimido en gzip
data = pd.read_csv("./steam3mill.csv.gz", compression="gzip")


# def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
# Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
# http://localhost:80/PlayTimeGenre/?genre=Action
@app.get("/PlayTimeGenre/")
def PlayTimeGenre(genre: str):
    # Filtramos por genero
    data_genres = data.dropna(subset=["genres"])
    data_genres = data_genres[data_genres["genres"].str.contains(genre)]
    # Agrupamos por año y sumamos las horas jugadas
    data_genres = (
        data_genres.groupby("release_date")["playtime_forever"].sum().reset_index()
    )
    # Obtenemos el año con mayor horas jugadas
    year = int(
        data_genres[
            data_genres["playtime_forever"] == data_genres["playtime_forever"].max()
        ]["release_date"].values[0]
    )
    return {"Año de lanzamiento con más horas jugadas para Género": genre, "Año": year}


# def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
# Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
# http://localhost:80/UserForGenre/?genre=Action
@app.get("/UserForGenre/")
def UserForGenre(genre: str):
    # Eliminar generos nulos
    data_genres = data.dropna(subset=["genres"])
    # Eliminar usuarios nulos
    data_genres = data_genres.dropna(subset=["user_id"])
    # Filtramos por genero
    data_genres = data_genres[data_genres["genres"].str.contains(genre)]
    # Agrupamos por usuario y sumamos las horas jugadas
    data_playtime = (
        data_genres.groupby("user_id")["playtime_forever"].sum().reset_index()
    )
    # Obtenemos el usuario con mayor horas jugadas
    user = data_playtime[
        data_playtime["playtime_forever"] == data_playtime["playtime_forever"].max()
    ]["user_id"].values[0]
    # Filtramos por usuario
    data_user = data_genres[data_genres["user_id"] == user]
    # Agrupamos por año y sumamos las horas jugadas
    data_year = (
        data_user.groupby("release_date")["playtime_forever"].sum().reset_index()
    )
    years = data_year.to_dict("records")
    # Obtenemos el año con mayor horas jugadas
    year = int(
        data_genres[
            data_genres["playtime_forever"] == data_genres["playtime_forever"].max()
        ]["release_date"].values[0]
    )
    print(
        f"'Usuario con más horas jugadas para Género {genre}': {user}, 'Horas jugadas': {years}"
    )


# def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
# Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
# http://localhost:80/UsersRecommend/?year=2013
@app.get("/UsersRecommend/")
def UsersRecommend(year: int):
    # Filtramos por año
    data_year = data[data["release_date"] == year]
    # Filtramos por recomendados
    data_year = data_year[data_year["recommend"] == True]
    # Filtramos por comentarios positivos/neutrales
    data_year = data_year[data_year["sentiment"] > 0]
    # Agrupamos por juego y contamos las recomendaciones
    data_year = data_year.groupby("app_name")["recommend"].count().reset_index()
    # Ordenamos de mayor a menor
    data_year = data_year.sort_values(by="recommend", ascending=False)
    # Obtenemos el top 3
    top3 = data_year.head(3).to_dict("records")
    return {
        "Top 3 de juegos MÁS recomendados por usuarios para el año": year,
        "Top 3": top3,
    }


# def UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
# Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
# http://localhost:80/UsersNotRecommend/?year=2013
@app.get("/UsersNotRecommend/")
def UsersNotRecommend(year: int):
    # Filtramos por año
    data_year = data[data["release_date"] == year]
    # Filtramos por no recomendados
    data_year = data_year[data_year["recommend"] == False]
    # Filtramos por comentarios negativos
    data_year = data_year[data_year["sentiment"] == 0]
    # Agrupamos por juego y contamos las recomendaciones
    data_year = data_year.groupby("app_name")["recommend"].count().reset_index()
    # Ordenamos de mayor a menor
    data_year = data_year.sort_values(by="recommend", ascending=False)
    # Obtenemos el top 3
    top3 = data_year.head(3).to_dict("records")
    return {
        "Top 3 de juegos MENOS recomendados por usuarios para el año": year,
        "Top 3": top3,
    }


# def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
# Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}
# http://localhost:80/sentiment_analysis/?year=2013
@app.get("/sentiment_analysis/")
def sentiment_analysis(year: int):
    # Filtramos por año
    data_year = data[data["release_date"] == year]
    # Agrupamos por sentimiento y contamos las reseñas
    data_year = data_year.groupby("sentiment")["review"].count().reset_index()
    # Obtenemos el top 3
    sentiment = data_year.to_dict("records")
    # Inicializar contadores
    negative_count = 0
    neutral_count = 0
    positive_count = 0
    # Contar el número de reseñas con cada sentimiento
    for s in sentiment:
        if s["sentiment"] == 0:
            negative_count += s["review"]
        elif s["sentiment"] == 1:
            neutral_count += s["review"]
        elif s["sentiment"] == 2:
            positive_count += s["review"]
    # Crear el diccionario con los contadores
    sentiment = {
        "Negative": negative_count,
        "Neutral": neutral_count,
        "Positive": positive_count,
    }
    return {"Según el año de lanzamiento": year, "Sentimiento": sentiment}


# Modelo de aprendizaje automático:
# Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning,
# y nuestro EDA nos permite entender bien los datos a los que tenemos acceso,
# es hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación.
# Para ello, te ofrecen dos propuestas de trabajo:
# En la primera, el modelo deberá tener una relación ítem-ítem, esto es se toma un item,
# en base a que tan similar esa ese ítem al resto, se recomiendan similares.
# Si es un sistema de recomendación item-item:
# def recomendacion_juego( id de producto ): Ingresando el id de producto,
# deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
# @app.get("/GameRecommendation/")
# def GameRecommendation(item_id: int):
#     # Cargar el modelo pickle
#     with open("model.pkl", "rb") as f:
#         model = pickle.load(f)
#     # Crear el DataFrame con los datos de entrada
#     input_df = pd.DataFrame([[item_id]], columns=["item_id"])
#     # Realizar la predicción con el modelo
#     try:
#         recommendations = model.recommend(input_df)
#     except:
#         raise HTTPException(status_code=400, detail="Invalid input")
#     # Devolver las recomendaciones
#     return recommendations
