#Importamos las librerias requeridas para el EDA

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import warnings
# from wordcloud import WordCloud, ImageColorGenerator
warnings.filterwarnings('ignore')
sns.set_theme()

# Importar steam
print("importando steam...")
steam = pd.read_csv('./assets/steam.csv')
# Visualizamos los datos
print(steam.shape)
steam.head(5)

#Informacion de los datos
steam.info()

#hacemos un conteo de los valores nulos
steam.isnull().sum()

# Realizamos una descripcion estadistica de los datos
steam.describe()

# Realizamos una descripcion estadistica de tipo texto
tipo_texto = steam.select_dtypes(include=['object']).columns
df_texto = steam[tipo_texto].describe()
print(df_texto.describe())

# Generamos un mapa de calor con las correlaciones de los datos
