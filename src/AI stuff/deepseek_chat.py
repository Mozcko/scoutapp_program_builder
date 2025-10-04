import os
import json
from openai import OpenAI, APIStatusError
from dotenv import load_dotenv
from pathlib import Path

# --- CONFIGURACIÓN ---
try:
    # Busca el .env en la raíz del proyecto
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except Exception as e:
    print(f"Advertencia: No se pudo cargar el archivo .env. Error: {e}")

# --- FUNCIONES AUXILIARES ---

def load_system_prompt(prompt_path: Path) -> str:
    """Carga el prompt del sistema desde un archivo de texto."""
    print(f"Cargando prompt del sistema desde: {prompt_path}...")
    try:
        if not prompt_path.is_file():
            raise FileNotFoundError(f"El archivo de prompt '{prompt_path.name}' no se encontró en la carpeta 'prompts'.")
        
        prompt = prompt_path.read_text(encoding='utf-8')
        print("¡Prompt del sistema cargado exitosamente!")
        return prompt
    except Exception as e:
        raise RuntimeError(f"No se pudo leer el archivo de prompt: {e}")

def setup_client() -> OpenAI:
    """Configura y devuelve el cliente de OpenAI para la API de DeepSeek."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("No se encontró la DEEPSEEK_API_KEY. Revisa tu archivo .env.")
    
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

def load_context_chunks(index_path: Path) -> list[str]:
    """Carga los trozos de contexto desde el archivo de índice JSON."""
    print(f"Cargando índice de contexto desde: {index_path}...")
    try:
        if not index_path.is_file():
            raise FileNotFoundError(
                f"El archivo de índice '{index_path.name}' no se encontró. "
                "Por favor, ejecuta 'python create_index.py' para generarlo."
            )
        
        with open(index_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        print(f"¡Índice cargado! {len(chunks)} trozos de conocimiento disponibles.")
        return chunks
    except Exception as e:
        raise RuntimeError(f"No se pudo leer el archivo de índice: {e}")

def find_relevant_context(query: str, chunks: list[str], top_k: int = 5) -> str:
    """Encuentra los 'top_k' trozos de contexto más relevantes para una consulta."""
    query_words = set(query.lower().split())
    if not query_words:
        return ""

    scores = []
    for i, chunk in enumerate(chunks):
        chunk_words = set(chunk.lower().split())
        common_words = query_words.intersection(chunk_words)
        score = len(common_words)
        if score > 0:
            scores.append((score, i))
    
    scores.sort(reverse=True)
    top_indices = [i for score, i in scores[:top_k]]
    
    relevant_chunks = [chunks[i] for i in top_indices]
    
    if relevant_chunks:
        print(f"-> Se encontraron {len(relevant_chunks)} trozos de contexto relevantes para la consulta.")
    
    return "\n---\n".join(relevant_chunks)

def create_system_prompt_with_context(base_prompt: str, relevant_context: str) -> dict:
    """Crea el mensaje del sistema para la API."""
    system_content = f"""
{base_prompt}

---
4. Conocimiento Relevante para la Pregunta Actual
Usa la siguiente información de tus archivos para responder la pregunta del usuario.

CONTEXTO RELEVANTE:
{relevant_context if relevant_context else "No se encontró contexto relevante en los archivos para esta pregunta."}
---
"""
    return {"role": "system", "content": system_content}

def run_chat_loop(client: OpenAI, context_chunks: list[str], base_prompt: str):
    """Maneja el bucle principal de la conversación en la consola."""
    historial_mensajes = [] 
    
    print("\n¡Conexión exitosa! El Scout Program Builder está listo.")
    print("Para comenzar, escribe algo como 'Quiero empezar a diseñar un programa'.")
        
    while True:
        try:
            user_prompt = input("\nTú: ")
            if user_prompt.lower() in ['salir', 'exit', 'quit']:
                print("¡Siempre listos para servir! ¡Hasta luego!")
                break
            
            historial_mensajes.append({"role": "user", "content": user_prompt})
            
            relevant_context = find_relevant_context(user_prompt, context_chunks)
            
            system_message = create_system_prompt_with_context(base_prompt, relevant_context)
            
            messages_to_send = [system_message] + historial_mensajes
            
            print("\nScout Program Builder está pensando...")

            chat_completion = client.chat.completions.create(
                model="deepseek-coder",
                messages=messages_to_send,
                max_tokens=4096,
                temperature=0.7, 
            )
            
            ai_response = chat_completion.choices[0].message.content
            
            historial_mensajes.append({"role": "assistant", "content": ai_response})

            print(f"\nScout Program Builder: {ai_response}")

        except APIStatusError as e:
            # ... (manejo de errores)
            print(f"Error de API: {e.message}")
            break
        except Exception as e:
            print(f"\nOcurrió un error inesperado: {e}")
            break

# --- FUNCIÓN PRINCIPAL ---

def main():
    """Punto de entrada principal del script."""
    print("Iniciando Scout Program Builder...")
    
    try:
        client = setup_client()
        
        # Carga el prompt base desde el archivo de texto
        prompt_path = Path(__file__).parent.parent / 'prompt.txt'
        base_prompt = load_system_prompt(prompt_path)

        # Carga el conocimiento desde el índice
        index_path = Path(__file__).parent.parent / 'context_index.json'
        context_chunks = load_context_chunks(index_path)

        # Inicia el chat
        run_chat_loop(client, context_chunks, base_prompt)

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"\nError de inicio: {e}")
    except Exception as e:
        print(f"\nOcurrió un error crítico durante el inicio: {e}")

if __name__ == "__main__":
    main()

