# Importacion de librerias
import pandas as pd
import numpy as np
import json
import re
import gzip
import ast
import warnings
from textblob import TextBlob
warnings.filterwarnings('ignore')


# Importar users_items
rows = []
with gzip.open('./assets/users_items.json.gz', 'rt', encoding='utf8') as f:
    print("importando users_items...")
    for line in f.readlines():        
        data_dic = ast.literal_eval(line)
        user_id = data_dic['user_id']
        # items_count = data_dic['items_count']
        steam_id = data_dic['steam_id']
        # user_url = data_dic['user_url']
        items_list = data_dic['items']
        data_list = []
        for items in items_list:
            data = {
                'user_id': user_id, 
                # items_count, 
                'steam_id': steam_id
                #, user_url
            }     
            for key, value in items.items():
                data.update({key:value})
            rows.append(data)
# print("insertamos los datos en un DataFrame...")
users_items = pd.DataFrame(rows)
users_items.to_csv('./assets/users_items.csv', index=False)


# Importar users_reviews
rows = []
with gzip.open('./assets/user_reviews.json.gz', 'rt', encoding='utf8') as f:
    print("importando user_reviews...")
    for line in f.readlines():        
        data_dic = ast.literal_eval(line)
        user_id = data_dic['user_id']
        # user_url = data_dic['user_url']
        reviews_list = data_dic['reviews']
        data_list = []
        for reviews in reviews_list:
            # analisis de sentimientos
            if reviews["review"] == "":
                sentiment_analysis = 1
            else:
                review_text = reviews["review"]
                if review_text == "":
                    sentiment_analysis = 1
                else:
                    blob = TextBlob(review_text)
                    sentiment_polarity = blob.sentiment.polarity
                    if sentiment_polarity < -0.1:
                        sentiment_analysis = 0
                    elif sentiment_polarity > 0.1:
                        sentiment_analysis = 2
                    else:
                        sentiment_analysis = 1
            data = {
                'user_id': user_id, 
                # user_url,
                'recommend': reviews["recommend"],
                'sentiment': sentiment_analysis,
                'item_id': reviews['item_id'],
                'review': reviews['review'],
            }  
            # agregar todos los campos de reviews   
            # for key, value in reviews.items():
            #     data.update({key:value})
            rows.append(data)
users_reviews = pd.DataFrame(rows)
users_reviews.to_csv('./assets/users_reviews.csv', index=False)


# Importar steam_games
years = range(1950, 2024)
rows = []
with gzip.open('./assets/steam_games.json.gz', 'rt', encoding='utf8') as f:
    print("importando steam_games...")
    for line in f.readlines():
        # Lee el archivo JSON
        data_json = json.loads(line)
        # Convierte el JSON en un diccionario
        data_dic = dict(data_json)
        # si id es NaN termino la ejecución
        if str(data_dic['id']) != "nan":
            data={
                'publisher': data_dic['publisher'],
                'genres': data_dic['genres'],
                'app_name': data_dic['app_name'],
                'release_date': data_dic['release_date'],
                'price': data_dic['price'],
                'item_id': data_dic['id'],
            }
            for key, value in data_dic.items():        
                # si el precio no es float lo reemplazo por 0
                if key == "price": 
                    if isinstance(value, float) and value > 0:
                        data.update({key: value})
                    else:
                        data.update({key: 0})
                # si el año no esta en el rango lo reemplazo por None
                if key == "release_date":
                    if not isinstance(value, str):
                        data.update({key:None})                     
                    else:
                        # Buscar el año dentro de la cadena de texto utilizando una expresión regular
                        patron = r"\b(19[5-9]\d|20\d{2})\b"
                        match = re.search(patron, value)
                        # Si se encuentra un año dentro del rango, reemplazarlo por el mismo
                        if match:
                            year = int(match.group(0))
                            if year in years:
                                data.update({key:year})
                            else:
                                data.update({key:None})
                        else:
                            data.update({key:None})
                # si esta en data y es nan lo reemplazo por None
                if key in data and str(value).find("nan") != -1:
                    data.update({key:None})
            rows.append(data)
steam_games = pd.DataFrame(rows)
steam_games.to_csv('./assets/steam_games.csv', index=False)


# Importar users_items de csv
print("importando users_items...")
users_items = pd.read_csv('./assets/users_items.csv')
# Importar users_reviews de csv
print("importando users_reviews...")
users_reviews = pd.read_csv('./assets/users_reviews.csv')
# Importar steam_games de csv
print("importando steam_games...")
steam_games = pd.read_csv('./assets/steam_games.csv')
# uno los tres dataframes
print("unificando los dataframes...")
df = pd.merge(steam_games, users_items, on=['item_id'], how='inner')
df = pd.merge(df, users_reviews, on=['user_id'], how='inner')
# guardo el dataframe en un archivo csv
print("guardando el dataframe en un archivo csv...")
df.to_csv('./assets/steam.csv', index=False)
print("termino la importación!!!")


# Importar steam
print("importando steam...")
data = pd.read_csv('./assets/steam.csv')
# Mostrar los primeros 5 registros
print("Mostrar los primeros 5 registros...")
print(data.head())