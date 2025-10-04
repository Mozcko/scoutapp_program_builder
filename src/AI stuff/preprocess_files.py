import pypdf
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# --- CONFIGURACIÓN ---
SOURCE_FOLDER = Path(__file__).parent.parent.parent / 'context'
CACHE_FOLDER = Path(__file__).parent.parent.parent / 'cache' # Carpeta para guardar el índice
CHUNK_SIZE = 512  # Tamaño de los fragmentos de texto en caracteres
CHUNK_OVERLAP = 50 # Superposición para no perder contexto entre fragmentos

# Modelo para crear los embeddings. 'all-MiniLM-L6-v2' es ligero y multilingüe.
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

def read_all_text_from_source() -> str:
    """Lee y extrae texto de todos los archivos en la carpeta de contexto."""
    print(f"1. Leyendo archivos desde: {SOURCE_FOLDER}...")
    if not SOURCE_FOLDER.is_dir():
        raise FileNotFoundError(f"La carpeta de contexto '{SOURCE_FOLDER}' no existe.")

    full_text = []
    for archivo in sorted(SOURCE_FOLDER.iterdir()):
        if not archivo.is_file():
            continue
        try:
            if archivo.suffix.lower() == '.pdf':
                reader = pypdf.PdfReader(archivo, strict=False)
                texto_paginas = [p.extract_text() for p in reader.pages if p.extract_text()]
                full_text.append("\n".join(texto_paginas))
            else:
                full_text.append(archivo.read_text(encoding='utf-8', errors='ignore'))
        except Exception as e:
            print(f"  - Advertencia: No se pudo leer el archivo {archivo.name}: {e}")
    print("  Lectura de archivos completada.")
    return "\n\n".join(full_text)

def split_text_into_chunks(text: str) -> list[str]:
    """Divide el texto completo en fragmentos más pequeños."""
    print("2. Dividiendo el texto en fragmentos (chunks)...")
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    print(f"  Se crearon {len(chunks)} fragmentos.")
    return chunks

def create_and_save_index(chunks: list[str]):
    """Crea embeddings y guarda el índice FAISS y los fragmentos de texto."""
    print(f"3. Creando embeddings con el modelo '{EMBEDDING_MODEL}' (esto puede tardar)...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(chunks, show_progress_bar=True)
    
    if not embeddings.any():
        raise ValueError("No se pudieron generar embeddings. ¿Los archivos de contexto están vacíos?")

    # Crear índice FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Crear la carpeta de caché si no existe
    CACHE_FOLDER.mkdir(exist_ok=True)
    
    # Guardar el índice y los fragmentos
    faiss.write_index(index, str(CACHE_FOLDER / "context.faiss"))
    with open(CACHE_FOLDER / "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
        
    print("4. ¡Índice y fragmentos guardados exitosamente en la carpeta 'cache'!")

def main():
    """Flujo principal del preprocesamiento."""
    try:
        full_text = read_all_text_from_source()
        if not full_text.strip():
            print("No se encontró texto en los archivos de contexto. Abortando.")
            return
        chunks = split_text_into_chunks(full_text)
        create_and_save_index(chunks)
        print("\nPreprocesamiento finalizado. Ya puedes ejecutar la aplicación de chat.")
    except Exception as e:
        print(f"\nOcurrió un error durante el preprocesamiento: {e}")

if __name__ == "__main__":
    main()