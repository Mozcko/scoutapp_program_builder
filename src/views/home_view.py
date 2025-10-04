import flet as ft
from components.app_bar import main_app_bar

class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/"
        self.appbar = main_app_bar()
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Bienvenido al Scout Program Builder",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Tu asistente inteligente para crear programas Scout.",
                            size=16,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.FilledButton(
                            "¡Empezar a chatear!",
                            icon=ft.Icons.CHAT_BUBBLE_ROUNDED,
                            on_click=lambda _: self.page.go("/chat"),
                            height=50,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=25,
                ),
                width=800, # Ancho máximo para el contenido
                padding=20, # Añade un poco de espacio en los bordes
                alignment=ft.alignment.center,
            )
        ]