import flet as ft
from views.chat_view import ChatView
from views.home_view import HomeView

def main(page: ft.Page):
    page.title = "Scout Program Builder"
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.theme_mode = ft.ThemeMode.DARK

    # Diccionario de vistas para el enrutamiento
    views = {
        "/": HomeView(page),
        "/chat": ChatView(page),
    }

    def route_change(route):
        page.views.clear()
        # Obtiene la vista correspondiente a la ruta, o la de inicio si no se encuentra
        view = views.get(page.route, views["/"])
        page.views.append(view)
        page.go(page.route)

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    # Inicia la aplicación en modo servidor web, lista para producción
    ft.app(target=main, port=8502, host="0.0.0.0")
