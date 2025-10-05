import os
import faiss
import pickle
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# --- CONFIGURACIÓN Y CARGA INICIAL ---
print("DEBUG: [1] Iniciando carga de chat_controller.")

# Cargar variables de entorno
try:
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except Exception:
    print("Advertencia: No se pudo cargar el archivo .env.")
print("DEBUG: [2] Carga de .env intentada.")

# Cargar el prompt base
try:
    prompt_path = Path(__file__).parent.parent.parent / 'prompt.txt'
    BASE_PROMPT = prompt_path.read_text(encoding='utf-8')
except Exception:
    BASE_PROMPT = "Eres un asistente servicial."
    print("Advertencia: No se pudo cargar el prompt. Se usará uno por defecto.")
print("DEBUG: [3] Carga de prompt.txt intentada.")

# Cargar el índice RAG (FAISS y chunks)
faiss_index = None
chunks = []
try:
    print("DEBUG: [4] Intentando cargar índice FAISS y chunks.")
    cache_folder = Path(__file__).parent.parent.parent / 'cache'
    faiss_index = faiss.read_index(str(cache_folder / "context.faiss"))
    with open(cache_folder / "chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    print("DEBUG: [5] Carga de índice FAISS y chunks completada.")
except Exception as e:
    print(f"DEBUG: [5-ERROR] Error al cargar índice: {e}")

# Cargar el modelo de embeddings
embedding_model = None
try:
    print("DEBUG: [6] Intentando cargar modelo de embeddings SentenceTransformer.")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("DEBUG: [7] Carga de modelo de embeddings completada.")
except Exception as e:
    print(f"DEBUG: [7-ERROR] Error al cargar modelo: {e}")

print("DEBUG: [8] Carga de chat_controller finalizada.")

# --- CLASE DEL CONTROLADOR ---

class ChatController:
    """
    Maneja toda la lógica de la conversación con la IA.
    """
    def __init__(self):
        self._client = self._setup_client()
        self._historial_mensajes = []

    def _setup_client(self) -> OpenAI:
        api_key = os.getenv("API_KEY")
        if not api_key:
            error_msg = "---\n--- FATAL ERROR: La variable de entorno API_KEY no fue encontrada. Por favor, configúrala en Railway. ---\n---"
            print(error_msg)
            raise ValueError(error_msg)
        return OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

    def _find_relevant_context(self, query: str, top_k: int = 3) -> str:
        if not faiss_index or not embedding_model or not chunks:
            return "El sistema de búsqueda de contexto no está disponible."
        
        query_embedding = embedding_model.encode([query])
        distances, indices = faiss_index.search(query_embedding, top_k)
        
        relevant_chunks = [chunks[i] for i in indices[0]]
        return "\n---\n".join(relevant_chunks)

    def get_ai_response(self, user_prompt: str) -> str:
        """
        Obtiene una respuesta de la IA basándose en el prompt del usuario y el contexto.
        """
        try:
            self._historial_mensajes.append({"role": "user", "content": user_prompt})
            
            relevant_context = self._find_relevant_context(user_prompt)
            
            system_content = f"{BASE_PROMPT}\n\n--- CONTEXTO RELEVANTE ---\n{relevant_context}"
            system_message = {"role": "system", "content": system_content}
            
            messages_to_send = [system_message] + self._historial_mensajes

            response = self._client.chat.completions.create(
                model="deepseek-coder",
                messages=messages_to_send,
                max_tokens=4096,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content
            self._historial_mensajes.append({"role": "assistant", "content": ai_response})
            
            return ai_response

        except Exception as e:
            error_message = f"Ocurrió un error: {e}"
            print(error_message)
            return error_message