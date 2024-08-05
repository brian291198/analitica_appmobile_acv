import flet as ft
from flet import *
from home import home_view
from welcome import welcome_view
from objetive1 import objetive1_view
from objetive2 import objetive2_view
from objetive3 import objetive3_view
from ia_chatbot import chatbot
from login import login_view
from register import registration_view

#administrar rutas de la APP
class AppState:
    def __init__(self):
        self.page = None

    def set_page(self, page):
        self.page = page

    def show_home(self):
        if self.page:
            home_view(self.page, self)

    def show_login(self):
        if self.page:
            login_view(self.page, self)

    def show_register(self):
        if self.page:
            registration_view(self.page, self)

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
    def show_chatbot(self):
        if self.page:
            chatbot(self.page, self)


def main (page: ft.Page):

    #Configuraciones de la interfaz en general
    page.title = "App de predicción de ACV"
    page.window.width = 360  # Ajusta esto según el dispositivo
    page.window.height = 720
    page.bgcolor = "#dddddd"


    page.fonts={
        "Comfortaa-Light": "Comfortaa-Light.ttf",
        "Comfortaa-Regular": "Comfortaa-Regular.ttf",
        "Comfortaa-Bold": "Comfortaa-Bold.ttf",

        "LTSaeada-1":"/fonts/LTSaeada/3-LTSaeada-ExtraLight.otf",
        "LTSaeada-2":"/fonts/LTSaeada/5-LTSaeada-Regular.otf",
        "LTSaeada-3":"/fonts/LTSaeada/7-LTSaeada-SemiBold.otf",
        "LTSaeada-4":"/fonts/LTSaeada/8-LTSaeada-Bold.otf",
        "LTSaeada-5":"/fonts/LTSaeada/11-LTSaeada-ExtraBlack.otf",

        "RoundsNeue-1":"/fonts/RoundsNeue/TT Rounds Neue Trial Light.ttf",
        "RoundsNeue-2":"/fonts/RoundsNeue/TT Rounds Neue Trial Regular.ttf",
        "RoundsNeue-3":"/fonts/RoundsNeue/TT Rounds Neue Trial Bold.ttf",
        "RoundsNeue-4":"/fonts/RoundsNeue/TT Rounds Neue Trial Black.ttf"
    }


    page.theme = ft.Theme(font_family="RoundsNeue-2")
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment="center"
    page.vertical_alignment="center"



    app_state = AppState()
    app_state.set_page(page)
    app_state.show_login()  # Muestra la vista principal al iniciar

ft.app(target=main, assets_dir="assets")
 