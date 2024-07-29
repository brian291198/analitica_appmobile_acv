import flet as ft
from flet import *

def navigator_component(page, app_state):


    def ver_home(e):
        page.controls.clear()
        app_state.show_home()
        page.update()

    def ver_objetivo1(e):
        page.controls.clear()
        app_state.show_objetive1()
        page.update()

    def ver_resultados(e):
        pass

    def on_navigation_change(e):
        if e.control.selected_index == 0:
            ver_home(e)
        elif e.control.selected_index == 1:
            ver_objetivo1(e)
        elif e.control.selected_index == 2:
            ver_resultados(e)

 
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explorar"),
            ft.NavigationBarDestination(icon=ft.icons.ONLINE_PREDICTION, label="Predecir"),
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Resultados",
            ),
        ], 
        bgcolor=ft.colors.BLUE_600,
        on_change=on_navigation_change,
        indicator_color=ft.colors.BLUE_300
    )





