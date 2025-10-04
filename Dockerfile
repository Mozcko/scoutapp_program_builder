# 1. Usar una imagen base de Python
FROM python:3.10-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app

# 3. Copiar todos los archivos del proyecto (respetando .dockerignore)
COPY . .

# 4. Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Ejecutar el script de pre-procesamiento para generar el índice y descargar el modelo
# Esto se hace durante la construcción de la imagen, no cada vez que se ejecuta
RUN python "src/AI stuff/preprocess_files.py"

# 6. Exponer el puerto que la aplicación usará
EXPOSE 8502

# 7. Definir el comando para ejecutar la aplicación
CMD ["python", "src/main.py"]