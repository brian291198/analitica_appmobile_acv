import flet as ft
from flet import *
import requests
from login import login_view
from datetime import datetime
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered, desplegable_diagnostico
from menubar import menubar

def view_data_diagnostico(page, app_state):

    page.padding=0

    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return
    #Obtener token
    token =app_state.token

    global prediccion_resultado  
    #API_URL = 'http://127.0.0.1:8080/api/acv1/'

    def view_chart(e, page, app_state):
            page.controls.clear()
            menu_bar=menubar(page, app_state)
            page.controls.append(menu_bar)
            page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
            app_state.show_chart()
            page.update()

    # Crear registros ficticios (definidos arriba)
    registros = [
    {
        "idDiagnostico": 101,
        "fechaRegistro": "2024-08-01",
        "Genero": "Masculino",
        "Edad": "45",
        "Hipertension": "Sí",
        "Cardiopatia": "No",
        "TipoTrabajo": "Oficina",
        "Nivel_GlucosaPromedio": "120",
        "ICM": "24.5",
        "EstadoFumador": "No",
        "Prediccion": "Bajo riesgo"
    },
    {
        "idDiagnostico": 102,
        "fechaRegistro": "2024-08-05",
        "Genero": "Femenino",
        "Edad": "50",
        "Hipertension": "No",
        "Cardiopatia": "Sí",
        "TipoTrabajo": "Campo",
        "Nivel_GlucosaPromedio": "110",
        "ICM": "22.0",
        "EstadoFumador": "Sí",
        "Prediccion": "Alto riesgo"
    },
    {
        "idDiagnostico": 103,
        "fechaRegistro": "2024-08-10",
        "Genero": "Masculino",
        "Edad": "60",
        "Hipertension": "Sí",
        "Cardiopatia": "Sí",
        "TipoTrabajo": "Oficina",
        "Nivel_GlucosaPromedio": "130",
        "ICM": "30.0",
        "EstadoFumador": "Sí",
        "Prediccion": "Moderado riesgo"
    },
    {
        "idDiagnostico": 104,
        "fechaRegistro": "2024-08-15",
        "Genero": "Femenino",
        "Edad": "55",
        "Hipertension": "No",
        "Cardiopatia": "No",
        "TipoTrabajo": "Hogar",
        "Nivel_GlucosaPromedio": "115",
        "ICM": "25.0",
        "EstadoFumador": "No",
        "Prediccion": "Bajo riesgo"
    },
    {
        "idDiagnostico": 105,
        "fechaRegistro": "2024-08-20",
        "Genero": "Masculino",
        "Edad": "65",
        "Hipertension": "Sí",
        "Cardiopatia": "Sí",
        "TipoTrabajo": "Campo",
        "Nivel_GlucosaPromedio": "140",
        "ICM": "32.5",
        "EstadoFumador": "Sí",
        "Prediccion": "Alto riesgo"
    }
    ]


    # Crear una lista de ExpansionTile para cada registro
    tiles = []
    for registro in registros:
        tile = ft.ExpansionTile(
            title=ft.Text(f"Diagnóstico N° {registro['idDiagnostico']}       {registro['fechaRegistro']}", color=color_primary, size=17),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            bgcolor=desplegable_diagnostico,
            #collapsed_text_color=ft.colors.WHITE,
            text_color=ft.colors.RED,
            controls=[
                      ft.ListTile(title=ft.Text(f"Hipertension: {registro['Hipertension']}", color=color, size=14), height=40),
                      ft.ListTile(title=ft.Text(f"Cardiopatia: {registro['Cardiopatia']}", color=color, size=14), height=40),
                      ft.ListTile(title=ft.Text(f"Tipo de Trabajo: {registro['TipoTrabajo']}", color=color, size=14), height=40),
                      ft.ListTile(title=ft.Text(f"Nivel de Glucosa Promedio: {registro['Nivel_GlucosaPromedio']}", color=color, size=14), height=40),
                      ft.ListTile(title=ft.Text(f"ICM: {registro['ICM']}", color=color, size=14), height=40),
                      ft.ListTile(title=ft.Text(f"Estado Fumador: {registro['EstadoFumador']}", color=color, size=14), height=40),
                      ft.ListTile(title=ft.Text(f"Predicción: {registro['Prediccion']}", color=color, size=14), height=40),
                      ],
            )
        tiles.append(tile)

        list_data=ft.Container(content=ft.Column(
        controls=tiles
        ), width=300, margin=20)

        col_titulo=ft.Container(content=ft.Column(controls=[
             ft.Text("Registro de sus Diagnósticos", color= color, size=20, text_align="center")
        ],),width=300, margin=20,alignment=ft.alignment.center,  )

        btn_estadistica = ft.TextButton(
            on_click=lambda e: view_chart(e, page, app_state),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                    ft.Text("Estadísticas")
                ],  
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Color del texto
                bgcolor=color_primary,  # Color de fondo del botón (opcional)
                overlay_color=color_hovered,  # Color al hacer click o hover (opcional)
            ) 
            )

        btn_hipertension = ft.TextButton(
            #on_click=lambda e: logout(e, page, app_state, token),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                    ft.Text("Hipertensión")
                ],  
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Color del texto
                bgcolor=color_primary,  # Color de fondo del botón (opcional)
                overlay_color=color_hovered,  # Color al hacer click o hover (opcional)
            ) 
            )
        btn_cardiopatia = ft.TextButton(
            #on_click=lambda e: logout(e, page, app_state, token),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                    ft.Text("Cardiopatía")
                ],
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Color del texto
                bgcolor=color_primary,  # Color de fondo del botón (opcional)
                overlay_color=color_hovered,  # Color al hacer click o hover (opcional)
            ),       
            )
        btn_glucosa = ft.TextButton(
            #on_click=lambda e: logout(e, page, app_state, token),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                    ft.Text("Glucosa")
                ],
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Color del texto
                bgcolor=color_primary,  # Color de fondo del botón (opcional)
                overlay_color=color_hovered,  # Color al hacer click o hover (opcional)
            ),         
            )
        btn_imc = ft.TextButton(
            #on_click=lambda e: logout(e, page, app_state, token),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                    ft.Text("IMC")
                ],
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Color del texto
                bgcolor=color_primary,  # Color de fondo del botón (opcional)
                overlay_color=color_hovered,  # Color al hacer click o hover (opcional)
            ),         
            )
        btn_predicción = ft.TextButton(
            #on_click=lambda e: logout(e, page, app_state, token),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                    ft.Text("Predicción")
                ], 
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Color del texto
                bgcolor=color_primary,  # Color de fondo del botón (opcional)
                overlay_color=color_hovered,  # Color al hacer click o hover (opcional)
            ),         
            )
        

        row_estadistica=ft.Container(content=ft.Row([
             btn_estadistica
        ],alignment=ft.MainAxisAlignment.CENTER),padding=ft.padding.only(bottom=20), width=300,) #cambiar propiedad scroll por: scroll = ft.ScrollMode.HIDDEN para ocultar la barra de desplazamiento


        row_buttons=ft.Container(content=ft.Row([
             btn_hipertension, btn_cardiopatia, btn_glucosa, btn_imc, btn_predicción
        ],alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS),padding=20, width=300,) #cambiar propiedad scroll por: scroll = ft.ScrollMode.HIDDEN para ocultar la barra de desplazamiento

        list_buttons = ft.ListView(
        controls=[row_estadistica],
        )

        list_data_scrollable = ft.ListView(
        controls=[list_data],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
        )
    page.controls.append(col_titulo)
    page.controls.append(list_buttons)
    page.controls.append(list_data_scrollable)
    page.update()