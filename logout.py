import flet as ft
from flet import *
import requests

def logout_user(e):
        """ # Define la URL de la API de logout
        url = 'http://localhost:8080/logout/'  # Cambia a la URL de tu API
        # Asume que el token de autenticación es obtenido de alguna parte, por ejemplo, un estado global
        token = "tu-token-aqui"

        # Configura los headers de la solicitud
        headers = {
            "Authorization": f"Token {token}",
        }

        try:
            # Realiza la solicitud POST a la API de logout
            response = requests.post(url, headers=headers)

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Cierre de sesión exitoso!"))
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al cerrar sesión."), bg_color=ft.colors.RED)
                page.snack_bar.open = True
                page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bg_color=ft.colors.RED)
            page.snack_bar.open = True
            page.update() """

def logout_action(page, app_state):
    
    page.controls.append(ft.Text("probando LOGOUT"))
    page.update()