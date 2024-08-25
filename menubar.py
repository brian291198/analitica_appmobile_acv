import flet as ft
from flet import *
from login import login_view
import requests
from styles import color, color_hint, color_primary, color_secondary, color_hovered
from urlsapi import HTTP_LOGOUT

#APLICANDO EL LOGOUT Y OTRAS OPCIONES DEL MENÚ SUPERIOR

def logout_user(e, page, token):
            global token_delete
            # Define la URL de la API de logout
            url = HTTP_LOGOUT  # Cambia a la URL de tu API

            # Configura los headers de la solicitud

            headers = {
                        'Authorization': f'Token {token}',
                        'Content-Type': 'application/json'}

            try:
                # Realiza la solicitud POST a la API de logout
                response = requests.post(url, headers=headers)

                # Verifica si la solicitud fue exitosa
                if response.status_code == 200:
                    response_json = response.json()
                    token_delete = response_json.get('token')
                    page.snack_bar = ft.SnackBar(ft.Text("Cierre de sesión exitoso!", color=ft.colors.WHITE))
                    page.snack_bar.bgcolor = color_primary
                    page.snack_bar.open = True
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Error al cerrar sesión.", color=ft.colors.WHITE))
                    page.snack_bar.bgcolor = ft.colors.RED_300
                    page.snack_bar.open = True
                    page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}", color=ft.colors.WHITE))
                page.snack_bar.bgcolor = ft.colors.RED_300
                page.snack_bar.open = True
                page.update()

def logout (e, page, app_state, token):
     
            logout_user(e, page, token)
            page.navigation_bar.visible = not page.navigation_bar.visible
            if not token_delete:
                # Si no hay token, redirigir al inicio de sesión
                page.controls.clear()
                login_view(page, app_state)
                page.update()
            return
        

def menubar(page, app_state):

    #Obtener token
    token =app_state.token

    icon_boton = ft.TextButton(
            on_click=lambda e: logout(e, page, app_state, token),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.EXIT_TO_APP, color=color_primary, size=20),
                ],
                #alignment=ft.MainAxisAlignment.CENTER,   
            ),       
            )
    
    col_icon=ft.Container(content=ft.Row([
                icon_boton
            ], alignment=ft.MainAxisAlignment.END,
            ), expand=True, 
            height=50,
            #padding=10, 
            bgcolor=ft.colors.WHITE,
            )

    menubar = ft.Container(content=ft.Row([
           col_icon
            ]
            ), expand=True,
            height=50,
            bgcolor=ft.colors.WHITE,
            margin=ft.margin.only(bottom=-2),
            )

    return ft.Row([menubar])