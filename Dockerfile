# Usa una imagen base de Python (basada en Debian)
FROM python:3.11-slim-bookworm

# Instala las dependencias del sistema operativo que Flet necesita.
# Esto incluye GTK3 y GStreamer para el renderizado y multimedia.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    libmpv2 \
    xvfb \
    xauth \
    # Crea un symlink para que Flet encuentre libmpv.so.1 aunque instalemos libmpv2
    && ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Crea un usuario no-root para ejecutar la aplicación
RUN useradd --create-home --shell /bin/bash appuser

# Añade el directorio de binarios del usuario al PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Cambia al usuario no-root
USER appuser

# Copia primero el archivo de requerimientos para aprovechar el caché de Docker
COPY requirements.txt requirements.txt

# Instala las dependencias de Python
# Ahora se ejecuta como 'appuser'
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu aplicación al contenedor
COPY . .

# Expone el puerto que usará Flet
EXPOSE 8502

# El comando para iniciar la aplicación web de Flet
CMD ["xvfb-run", "python3", "src/main.py"]