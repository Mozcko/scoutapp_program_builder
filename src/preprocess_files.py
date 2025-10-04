import pypdf
from pathlib import Path

# Define las rutas relativas al script
# Asume que este script se ejecuta desde la raíz del proyecto
SOURCE_FOLDER = Path(__file__).parent.parent / 'context'
CACHE_FILE = Path(__file__).parent / 'processed_context.txt'

def preprocess_files():
    """
    Lee todos los archivos de la carpeta de contexto, extrae el texto,
    y guarda el resultado combinado en un único archivo de caché.
    """
    print(f"Iniciando preprocesamiento de archivos desde: {SOURCE_FOLDER}...")

    if not SOURCE_FOLDER.is_dir():
        print(f"ERROR: La carpeta de contexto '{SOURCE_FOLDER}' no existe. No se puede continuar.")
        return

    archivos_a_procesar = [f for f in SOURCE_FOLDER.iterdir() if f.is_file()]
    total_archivos = len(archivos_a_procesar)
    
    if total_archivos == 0:
        print("No se encontraron archivos en la carpeta de contexto.")
        return

    print(f"Se encontraron {total_archivos} archivos para procesar.")
    contexto_completo = []

    for i, archivo in enumerate(sorted(archivos_a_procesar), 1):
        print(f"  [{i}/{total_archivos}] Procesando '{archivo.name}'...", end="", flush=True)
        contenido_archivo = ""
        try:
            if archivo.suffix.lower() == '.pdf':
                reader = pypdf.PdfReader(archivo, strict=False)
                texto_paginas = [page.extract_text() for page in reader.pages if page.extract_text()]
                contenido_archivo = "\n".join(texto_paginas)
            else:
                contenido_archivo = archivo.read_text(encoding='utf-8', errors='ignore')

            if contenido_archivo.strip():
                contexto_completo.append(f"--- INICIO DEL ARCHIVO: {archivo.name} ---\n")
                contexto_completo.append(contenido_archivo)
                contexto_completo.append(f"\n--- FIN DEL ARCHIVO: {archivo.name} ---\n\n")
                print(" OK")
            else:
                print(" Vacío (sin texto).")
        
        except Exception as e:
            print(f" ERROR ({type(e).__name__})")
    
    # Escribir el contenido combinado al archivo de caché
    try:
        CACHE_FILE.write_text("".join(contexto_completo), encoding='utf-8')
        print(f"\n¡Preprocesamiento finalizado! Contexto guardado en '{CACHE_FILE}'.")
    except Exception as e:
        print(f"\nError al guardar el archivo de caché: {e}")

if __name__ == "__main__":
    preprocess_files()
