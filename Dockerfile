# Usa una imagen base de Python
FROM python:3.13

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /src

# Copia primero el archivo de requerimientos para aprovechar el caché de Docker
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir .

# Copia todo el código de tu aplicación al contenedor
COPY . .

# Expone el puerto que usará Flet
EXPOSE 8502

# El comando para iniciar la aplicación web de Flet
CMD ["flet", "run", "--port", "8502", "--host", "0.0.0.0", "src/main.py"]
