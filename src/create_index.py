from pathlib import Path
import json

# --- CONFIGURACIÓN ---
# Apunta al archivo de texto preprocesado
SOURCE_FILE = Path(__file__).parent / 'processed_context.txt'
# El archivo de salida será nuestro "índice" en formato JSON
INDEX_FILE = Path(__file__).parent / 'context_index.json'

# Define el tamaño de cada "trozo" de texto (en caracteres)
CHUNK_SIZE = 2000
# Define cuántos caracteres se solapan entre trozos para no perder contexto
CHUNK_OVERLAP = 200

def create_index():
    """
    Lee el archivo de contexto procesado, lo divide en trozos manejables (chunks)
    y lo guarda como un índice en formato JSON.
    """
    print(f"Iniciando la creación del índice desde: {SOURCE_FILE}...")

    if not SOURCE_FILE.is_file():
        print(f"ERROR: El archivo de contexto '{SOURCE_FILE.name}' no existe.")
        print("Por favor, ejecuta 'python preprocess_files.py' primero.")
        return

    try:
        # Lee todo el contenido del archivo procesado
        full_text = SOURCE_FILE.read_text(encoding='utf-8')
        print(f"Archivo de contexto leído. Total de caracteres: {len(full_text)}")

        # Divide el texto en trozos (chunks)
        chunks = []
        start = 0
        while start < len(full_text):
            end = start + CHUNK_SIZE
            chunks.append(full_text[start:end])
            start += CHUNK_SIZE - CHUNK_OVERLAP
        
        print(f"El texto ha sido dividido en {len(chunks)} trozos.")

        # Guarda los trozos en un archivo JSON
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        
        print(f"\n¡Índice creado exitosamente! Se guardó en '{INDEX_FILE.name}'.")

    except Exception as e:
        print(f"\nOcurrió un error durante la creación del índice: {e}")

if __name__ == "__main__":
    create_index()
