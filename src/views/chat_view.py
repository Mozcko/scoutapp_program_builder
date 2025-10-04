import flet as ft
from models.chat_model import Message
from components.message_component import ChatMessage
from controllers.chat_controller import ChatController
from components.app_bar import main_app_bar

class ChatView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/chat"
        self.controller = ChatController()

        # UI Controls
        self.chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.new_message_field = ft.TextField(
            hint_text="Escribe tu mensaje...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=self.send_message_click,
        )

        self.controls = [
            main_app_bar(),
            ft.Container(
                content=self.chat_list,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    self.new_message_field,
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        tooltip="Enviar Mensaje",
                        on_click=self.send_message_click,
                    ),
                ],
            ),
        ]
        # Iniciar con un mensaje de bienvenida
        self.add_message("bot_message", "Scout Program Builder", "¡Hola! Para comenzar, escribe algo como 'Quiero empezar a diseñar un programa'.")

    def send_message_click(self, e):
        user_message = self.new_message_field.value
        if user_message.strip() == "":
            return

        # Limpiar el campo de texto y deshabilitar mientras se procesa
        self.new_message_field.value = ""
        self.new_message_field.disabled = True
        self.page.update()

        # Mostrar mensaje del usuario
        self.add_message("user_message", "Tú", user_message)

        # Obtener y mostrar respuesta de la IA
        ai_response = self.controller.get_ai_response(user_message)
        self.add_message("bot_message", "Scout Program Builder", ai_response)

        # Reactivar el campo de texto
        self.new_message_field.disabled = False
        self.page.update()
        self.new_message_field.focus()


    def add_message(self, msg_type: str, user_name: str, text: str):
        message = Message(user_name=user_name, text=text, message_type=msg_type)
        self.chat_list.controls.append(ChatMessage(message))
        self.page.update()
