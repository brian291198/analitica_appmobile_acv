import flet as ft
from flet import *
from styles import color, color_hint, color_primary, color_secondary, color_hovered
from menubar import menubar

def navigator_component(page, app_state):


    def ver_home(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_home()
        page.update()

    def ver_objetivo1(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_objetive1()
        page.update()
    
    def show_data_diagnostico(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_data_diagnostico()
        page.update()
    
    def ver_chatbot2(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_chatbot2()
        page.update()

    def on_navigation_change(e, page, app_state):
        if e.control.selected_index == 0:
            ver_home(e, page, app_state)
        elif e.control.selected_index == 1:
            show_data_diagnostico(e, page, app_state)
        elif e.control.selected_index == 2:
            ver_chatbot2(e, page, app_state)


 
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explorar"),
            ft.NavigationBarDestination(icon=ft.icons.STORAGE_ROUNDED, label="Registros"),
            ft.NavigationBarDestination(icon=ft.icons.AUTO_AWESOME_OUTLINED, label="IA"),
            #ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, selected_icon=ft.icons.BOOKMARK, label="IA",),
        ], 
        bgcolor=color_primary,
        on_change=lambda e: on_navigation_change(e, page, app_state),
        indicator_color=color_hovered,
        overlay_color=color_hovered,
        height=70
    )
    





