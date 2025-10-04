import flet as ft

def main_app_bar() -> ft.AppBar:
    """Crea y devuelve el AppBar principal para la aplicación."""
    return ft.AppBar(
        title=ft.Text("Scout Program Builder"),
        bgcolor=ft.Colors.TRANSPARENT,  # Se integra con el fondo de la página
    )