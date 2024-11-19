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
            url = HTTP_LOGOUT  

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
                    # Mostrar mensaje de éxito
                    snack_bar = ft.SnackBar(ft.Text("Cierre de sesión exitoso!", color=ft.colors.WHITE))
                    snack_bar.bgcolor = color_primary
                    page.overlay.append(snack_bar)  # Usar overlay para agregar el SnackBar
                    snack_bar.open = True  # Abrir el SnackBar
                    page.update()
                else:
                    # Mostrar mensaje de error
                    snack_bar = ft.SnackBar(ft.Text("Error al cerrar sesión.", color=ft.colors.WHITE))
                    snack_bar.bgcolor = ft.colors.RED_300
                    page.overlay.append(snack_bar)  # Usar overlay para agregar el SnackBar
                    snack_bar.open = True  # Abrir el SnackBar
                    page.update()
            except Exception as ex:
                # Mostrar mensaje de excepción
                snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}", color=ft.colors.WHITE))
                snack_bar.bgcolor = ft.colors.RED_300
                page.overlay.append(snack_bar)  # Usar overlay para agregar el SnackBar
                snack_bar.open = True  # Abrir el SnackBar
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

def go_setting(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_setting()
        page.update()

def menubar(page, app_state):
    #Obtener token
    token =app_state.token
    username = app_state.user_data.get('username', 'Usuario').upper()


    # Crear botón de cierre de sesión
    icon_logout = ft.TextButton(
        width=40,
        on_click=lambda e: logout(e, page, app_state, token),
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.EXIT_TO_APP, color=ft.colors.WHITE, size=24),  # Icono de salida en blanco
            ],
        ),       
    )
    
   # Crear fila con el ícono de usuario, nombre y el icono de logout alineados correctamente
    col_icon = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(name=ft.icons.PERSON, color=ft.colors.WHITE, size=20),  # Ícono de usuario
                    margin=ft.margin.only(left=15, right=5),  # Margen alrededor del ícono de usuario
                ),
                ft.Container(
                    content=ft.Text(username, color=ft.colors.WHITE, size=16, text_align=ft.TextAlign.LEFT),  # Nombre en mayúsculas
                    margin=ft.margin.only(left=3, right=10),  # Margen alrededor del nombre de usuario
                ),
                ft.Container(expand=True),  # Espacio flexible para empujar el icono de salida hacia la derecha
                icon_logout,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Alineación con espacio entre los elementos
        ),
        expand=True,
        height=50,
        margin=ft.margin.only(right=10),  # Margen derecho para el conjunto completo
        bgcolor="#6dbadc",  # Fondo de color especificado
    )

    # Crear barra de menú
    menubar = ft.Container(
        content=ft.Row([col_icon]),
        expand=True,
        height=50,
        bgcolor="#6dbadc",  # Fondo de color para la barra completa
        margin=ft.margin.only(bottom=-2),  # Sin espacio arriba
    )

    return ft.Row([menubar])