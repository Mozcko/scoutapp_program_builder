Esta es una aplicación multiplataforma que utiliza la IA de DeepSeek como motor principal, construida con Python y la librería Flet.

## Características

* Chat interactivo con la IA de DeepSeek.
* Capacidad de analizar archivos locales como contexto.
* Interfaz de usuario limpia y responsiva gracias a Flet.

## Configuración del Entorno de Desarrollo

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### Prerrequisitos

* Python 3.10 o superior
* Git

### Pasos de Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu_usuario/mi_app_deepseek.git](https://github.com/tu_usuario/mi_app_deepseek.git)
    cd mi_app_deepseek
    ```

2.  **(Recomendado) Crea y activa un entorno virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    # En Windows usa: .venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    El proyecto usa `pyproject.toml` para definir las dependencias. Instálalas con pip:
    ```bash
    pip install .
    ```
    O, si prefieres, desde `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura tu clave de API:**
    Crea un archivo llamado `.env` en la raíz del proyecto:
    ```bash
    touch .env
    ```
    Abre el archivo y añade tu clave de API de DeepSeek:
    ```
    API_KEY="tu_api_key_aqui"
    ```

## Cómo Ejecutar la Aplicación

Para ejecutar la versión de consola:
```bash
python python ./src/AI\ stuff/deepseek_chat.py
```

Para ejecutar la versión con interfaz gráfica (Flet):
```bash
flet run 
```

