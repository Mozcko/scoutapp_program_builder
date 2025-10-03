import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def main():
    """
    Función principal para iniciar un chat de consola con la API de DeepSeek.
    """
    print("Conectando con la API de DeepSeek...")

    try:
        # 1. Configuración del cliente
        # La librería de OpenAI es compatible con la API de DeepSeek.
        # Solo necesitamos apuntar a la URL base correcta y usar nuestra API key.
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )

        print("¡Conexión exitosa! Escribe tu pregunta o 'salir' para terminar.")
        
        # 2. Bucle de conversación
        while True:
            # Pedir input al usuario
            user_prompt = input("\nTú: ")

            # Condición para salir del bucle
            if user_prompt.lower() == 'salir':
                print("¡Hasta luego!")
                break
            
            # Mostrar un mensaje de espera
            print("DeepSeek está pensando...")

            # 3. Llamada a la API
            # Creamos la solicitud de completado de chat
            chat_completion = client.chat.completions.create(
                model="deepseek-chat",  # Modelo económico y potente para chat
                messages=[
                    {"role": "system", "content": "Eres un asistente servicial y conciso."},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2048, # Limita la longitud de la respuesta para controlar costos
                temperature=0.7, # Un valor balanceado para creatividad y coherencia
            )

            # 4. Mostrar la respuesta
            ai_response = chat_completion.choices[0].message.content
            print(f"\nDeepSeek: {ai_response}")

    except Exception as e:
        print(f"\nOcurrió un error: {e}")
        print("Asegúrate de que tu API key en el archivo .env es correcta.")

if __name__ == "__main__":
    main()

