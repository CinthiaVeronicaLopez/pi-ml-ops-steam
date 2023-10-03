# Usa la imagen oficial de Python 3.9 como base
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta actual al contenedor en /app
COPY . .

# Expone el puerto 80
EXPOSE 80

# Ejecuta el comando para iniciar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
