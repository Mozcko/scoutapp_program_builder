import flet as ft
from models.chat_model import Message

class ChatMessage(ft.Row):
    """
    Un componente para mostrar un solo mensaje en el chat.
    """
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START # Alinea el avatar y el texto verticalmente

        # Define el contenido del mensaje (Texto plano para el usuario, Markdown para el bot)
        if message.message_type == "user_message":
            message_content = ft.Text(message.text, selectable=True, color=ft.Colors.WHITE)
        else:  # Mensajes del bot
            message_content = ft.Markdown(
                value=message.text,
                selectable=True,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                code_theme="atom-one-dark",
                on_tap_link=lambda e: self.page.launch_url(e.data),
            )

        # Contenedor para la burbuja del mensaje
        message_bubble = ft.Container(
            content=ft.Column( # Columna para el nombre y el contenido
                controls=[
                    ft.Text(message.user_name, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    message_content
                ],
                spacing=4,
            ),
            padding=10,
            border_radius=15,
            margin=ft.margin.only(top=5, bottom=5),
            expand=True,
        )

        # Avatar del usuario
        user_avatar = ft.CircleAvatar(
            content=ft.Text(self._get_initials(message.user_name)),
            color=ft.Colors.WHITE,
            bgcolor=self._get_avatar_color(message.user_name),
        )

        # Alinea los mensajes del usuario a la derecha y los del bot a la izquierda
        if message.message_type == "user_message":
            self.alignment = ft.MainAxisAlignment.END
            message_bubble.bgcolor = ft.Colors.PRIMARY_CONTAINER
            self.controls = [message_bubble, user_avatar]
        else:  # Mensajes del bot
            self.alignment = ft.MainAxisAlignment.START
            message_bubble.bgcolor = ft.Colors.GREY_700 # Color gris oscuro para la burbuja del bot
            self.controls = [user_avatar, message_bubble]

    def _get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        return "A"

    def _get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.Colors.AMBER, ft.Colors.BLUE, ft.Colors.BROWN,
            ft.Colors.CYAN, ft.Colors.GREEN, ft.Colors.INDIGO,
            ft.Colors.LIME, ft.Colors.ORANGE, ft.Colors.PINK,
            ft.Colors.PURPLE, ft.Colors.RED, ft.Colors.TEAL,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
