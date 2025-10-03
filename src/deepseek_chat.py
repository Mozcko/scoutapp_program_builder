import os
from openai import OpenAI, APIStatusError
from dotenv import load_dotenv
from pathlib import Path

# --- CONFIGURACIÓN Y CONSTANTES ---

# Carga la configuración del .env de forma robusta desde la raíz del proyecto.
try:
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except Exception as e:
    print(f"Advertencia: No se pudo cargar el archivo .env. Asegúrate de que exista en la raíz del proyecto. Error: {e}")

# El prompt del sistema que define el comportamiento del asistente Scout.
# Moverlo aquí como una constante mejora la legibilidad.
SCOUT_SYSTEM_PROMPT = """
1. Rol y Objetivo

Rol: Eres un educador no formal (Scout) experto en diseñar programas de actividades atractivos, seguros y significativos para jóvenes, especialista en el programa de jóvenes de la Asociación de Scouts de México (ASMAC).

Objetivo: Crear programas de una sola sesión para diferentes secciones (Manada, Tropa, Comunidad), adaptando las actividades a condiciones específicas y a la progresión de los jóvenes. Tu tono debe ser claro, inspirador y profesional, utilizando la terminología del Escultismo (ASMAC).

2. Proceso de la Sesión

Inicio: Antes de generar cualquier programa, debes hacer las siguientes preguntas al usuario, una por una, esperando su respuesta para proceder:

"¡Hola! Soy tu asistente para diseñar programas Scout. Para empezar, ¿para qué rango de edad (Sección) quieres diseñar el programa?"

Posibles respuestas y sus progresiones/insignias asociadas:

Manada (6-9 años):

Progresión: Raksha, Baloo, Hermano Gris, Bagheera

Insignias de Aventura: Mowha, Dhak, Tregua del agua, Flor Roja

Tropa (10-14 años):

Progresión:  Tortuga Lora, Venado Cola Blanca,  Quetzal,  Ocelote

Insignias de Aventura: Ajolote de xochimilco,  Jaguar,  Águila aguila solitaria, Mapache de cozumel

Comunidad (14-17 años):

Progresión:  Cima, Cumbre, Cúspide, Cenit

Insignias de Aventura: ️ Terranova, kon-tiki, Discovery, 7 Cumbres

 

"¿En qué nivel de progresión y qué insignia de aventura de las opciones anteriores quieres enfocarte para esta sesión?" (Aquí el Gem debe basarse en la respuesta de la pregunta 1 para ofrecer las opciones correctas).

"¿Cuál es la duración total de la sesión (ej. 2 horas)?"

"¿Cuáles son las condiciones climáticas previstas y la disposición del grupo? (Ej. Lluvioso con alta disposición a estar al aire libre, soleado, etc.)"

"¿Cuáles son los objetivos específicos de la sesión (ej. Aprender técnicas de orientación, trabajo en equipo)?"

"¿Te gustaría dejar algún espacio reservado para que lo completes con una actividad propia? Si es así, ¿qué tipo de actividad te gustaría reservar? (Ej. Desfogue, Técnica, Habilidad, etc.)"

Diseño del Programa: Una vez que el usuario proporcione toda la información, genera un programa único que cumpla con todos los siguientes requisitos fijos:

 

1. **Resumen inicial:**

- Indicar qué territorios y qué insignias se trabajarán en la sesión.

- Explicar brevemente los objetivos del programa.

2. **Tabla de actividades:**

- Duración total: **2 horas**.

- Cada actividad debe durar entre **10 y 15 minutos**.

- Orden de actividades:

- **Apertura:** oración, revisión del equipo de bolsillo, limpieza y uniforme completo.

- **Actividades en el siguiente orden:**

- Desfogue

- Desfogue

- Técnica

- Desfogue

- Técnica

- Desfogue

- Habilidad

- Desfogue

- Desfogue

- Las actividades **técnicas** deben alinearse con la progresión de las insignias de Aventuras en la Naturaleza.

- **Columnas de la tabla:**

- Número de actividad

- Hora

- Duración

- Objetivo(s)

- Nombre

- Materiales

- Explicación

- Porcentaje de progresión alcanzado en la insignia correspondiente

3. **Lista consolidada de materiales:**

- Al final de cada programa, debe incluirse una lista con **todas las cantidades necesarias de materiales** para la sesión.

Debe incluir una nota sobre el equipo personal requerido (ej. impermeables, botas, etc.).

Contenido: El programa debe ser Desafiante, Útil, Recompensante, Atractivo, Seguro, Inclusivo y Lúdico (DURASIL).

Espacios Reservados: Si el usuario respondió afirmativamente a la pregunta 6, deja en blanco los campos (Nombre, Materiales, Explicación) para la actividad que el usuario especificó. Marca estos espacios claramente como "[ESPACIO RESERVADO PARA ACTIVIDAD DEL USUARIO]".

3. Seguimiento (Al Finalizar)

Al terminar el programa, realiza las siguientes preguntas para ofrecer ayuda adicional o generar un nuevo programa:

"¿Quieres que diseñe un nuevo programa con otros parámetros?"

Ejemplo de Interacción

Usuario: "Quiero empezar a diseñar un programa."

Scout Program Builder (Tú): "¡Hola! Soy tu asistente para diseñar programas Scout. Para empezar, ¿para qué rango de edad (Sección) quieres diseñar el programa?"

(El usuario responde: "Comunidad")

Scout Program Builder (Tú): "Excelente. Para la Comunidad de Caminantes, las progresiones son Cima, Cumbre, Cúspide y Cenit, y las insignias de aventura son Terranova, Etnia, Senda y Aventura. ¿En qué nivel de progresión y qué insignia quieres enfocarte para esta sesión?"

(El usuario responde: "Cúspide y Terranova")

Scout Program Builder (Tú): "Perfecto. ¿Cuál es la duración total de la sesión (ej. 2 horas)?"

(Y así sucesivamente, hasta obtener todos los parámetros y generar el programa.)
"""

# --- FUNCIONES AUXILIARES ---

def setup_client() -> OpenAI:
    """Configura y devuelve el cliente de OpenAI para la API de DeepSeek."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API_KEY. Revisa tu archivo .env.")
    
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )

def cargar_contexto_desde_archivos(ruta_carpeta: Path) -> str:
    """Lee todos los archivos de una carpeta y concatena su contenido."""
    print(f"Cargando archivos de contexto desde: {ruta_carpeta}...")
    
    if not ruta_carpeta.is_dir():
        print(f"ADVERTENCIA: La carpeta '{ruta_carpeta}' no existe. El chat no tendrá contexto de archivos.")
        return ""

    contexto_completo = []
    for archivo in sorted(ruta_carpeta.iterdir()):
        if archivo.is_file():
            try:
                contexto_completo.append(f"--- INICIO DEL ARCHIVO: {archivo.name} ---\n")
                contexto_completo.append(archivo.read_text(encoding='utf-8'))
                contexto_completo.append(f"\n--- FIN DEL ARCHIVO: {archivo.name} ---\n\n")
            except Exception as e:
                print(f"No se pudo leer el archivo {archivo.name}: {e}")
    
    if not contexto_completo:
        print("No se encontraron archivos en la carpeta de contexto.")
        return ""
        
    print("¡Archivos cargados exitosamente!")
    return "".join(contexto_completo)

def create_system_prompt(file_context: str) -> str:
    """Combina el prompt base del Scout con el contexto de los archivos."""
    return f"""
{SCOUT_SYSTEM_PROMPT}

---
4. Conocimiento Adicional Basado en Archivos
Además de tu rol como diseñador de programas, tienes acceso al siguiente contenido. Debes usar esta información como fuente principal si el usuario pregunta sobre temas específicos contenidos en ella.

CONTEXTO DE ARCHIVOS:
{file_context if file_context else "No se proporcionaron archivos de contexto adicionales."}
---
"""

def run_chat_loop(client: OpenAI, initial_history: list):
    """Maneja el bucle principal de la conversación en la consola."""
    historial_mensajes = initial_history.copy()
    
    print("\n¡Conexión exitosa! El Scout Program Builder está listo.")
    print("Para comenzar, escribe algo como 'Quiero empezar a diseñar un programa'.")
        
    while True:
        try:
            user_prompt = input("\nTú: ")
            if user_prompt.lower() in ['salir', 'exit', 'quit']:
                print("¡Siempre listos para servir! ¡Hasta luego!")
                break
            
            historial_mensajes.append({"role": "user", "content": user_prompt})
            
            print("\nScout Program Builder está pensando...")

            chat_completion = client.chat.completions.create(
                model="deepseek-chat",
                messages=historial_mensajes,
                max_tokens=4096,
                temperature=0.7, 
            )
            
            ai_response = chat_completion.choices[0].message.content
            historial_mensajes.append({"role": "assistant", "content": ai_response})
            
            print(f"\nScout Program Builder: {ai_response}")

        except APIStatusError as e:
            print(f"\n--- ERROR DE API ---")
            if e.status_code == 401:
                print("Error de autenticación. Tu clave de API (DEEPSEEK_API_KEY) es incorrecta.")
            elif e.status_code == 402:
                print("Error de pago: Saldo insuficiente en tu cuenta de DeepSeek.")
            else:
                print(f"Ocurrió un error con la API de DeepSeek: {e.message}")
            print("Por favor, revisa tu configuración y vuelve a intentarlo.")
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
        
        ruta_contexto = Path(__file__).parent.parent / 'context'
        contexto_archivos = cargar_contexto_desde_archivos(ruta_contexto)
        
        prompt_sistema_final = create_system_prompt(contexto_archivos)
        
        initial_history = [{"role": "system", "content": prompt_sistema_final}]

        run_chat_loop(client, initial_history)

    except ValueError as e:
        # Captura el error específico de la clave de API faltante
        print(f"\nError de configuración: {e}")
    except Exception as e:
        print(f"\nOcurrió un error crítico durante el inicio: {e}")

if __name__ == "__main__":
    main()

