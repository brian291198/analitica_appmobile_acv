import flet as ft
from flet import *
from home import home_view
from welcome import welcome_view
from objetive1 import objetive1_view
from objetive2 import objetive2_view
from objetive3 import objetive3_view

#administrar rutas de la APP
class AppState:
    def __init__(self):
        self.page = None

    def set_page(self, page):
        self.page = page

    def show_home(self):
        if self.page:
            home_view(self.page, self)

    def show_welcome(self):
        if self.page:
            welcome_view(self.page, self)
    
    def show_objetive1(self):
        if self.page:
            objetive1_view(self.page, self)
            
    def show_objetive2(self):
        if self.page:
            objetive2_view(self.page, self)
    
    def show_objetive3(self):
        if self.page:
            objetive3_view(self.page, self)

def main (page: ft.Page):

    #Configuraciones de la interfaz en general
    page.title = "App de predicción de ACV"
    page.window.width = 360  # Ajusta esto según el dispositivo
    page.window.height = 660
    page.bgcolor = "#dddddd"
    #fuente roboto
    page.fonts = {
        "Regular": "https://raw.githubusercontent.com/google/fonts/master/apache/opensans/OpenSans-Regular.ttf",
        "Bold": "https://raw.githubusercontent.com/google/fonts/master/apache/opensans/OpenSans-Bold.ttf"
    }
    page.theme = ft.Theme(font_family="Regular")

    app_state = AppState()
    app_state.set_page(page)
    app_state.show_welcome()  # Muestra la vista principal al iniciar

ft.app(target=main, assets_dir="assets")
 