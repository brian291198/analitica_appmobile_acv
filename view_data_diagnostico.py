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

    API_URL = 'http://127.0.0.1:8080/api/acv1/'

    registros=[]

    try:
        response = requests.get(API_URL, headers={'Authorization': f'Token {token}'})
        response.raise_for_status()  
        registros = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al obtener datos de la API: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error al hacer la solicitud a la API: {req_err}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    else:
        registros = registros if registros else []

    print(registros)

    global prediccion_resultado  
    #API_URL = 'http://127.0.0.1:8080/api/acv1/'

    def view_chart(e, page, app_state):
            page.controls.clear()
            menu_bar=menubar(page, app_state)
            page.controls.append(menu_bar)
            page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
            app_state.show_chart()
            page.update()

    # # Crear registros ficticios (definidos arriba)
    # registros = [
    # {
    #     "idDiagnostico": 101,
    #     "fechaRegistro": "2024-08-01",
    #     "Genero": "Masculino",
    #     "Edad": "45",
    #     "Hipertension": "Sí",
    #     "Cardiopatia": "No",
    #     "TipoTrabajo": "Oficina",
    #     "Nivel_GlucosaPromedio": "120",
    #     "ICM": "24.5",
    #     "EstadoFumador": "No",
    #     "Prediccion": "Bajo riesgo"
    # },
    # {
    #     "idDiagnostico": 102,
    #     "fechaRegistro": "2024-08-05",
    #     "Genero": "Femenino",
    #     "Edad": "50",
    #     "Hipertension": "No",
    #     "Cardiopatia": "Sí",
    #     "TipoTrabajo": "Campo",
    #     "Nivel_GlucosaPromedio": "110",
    #     "ICM": "22.0",
    #     "EstadoFumador": "Sí",
    #     "Prediccion": "Alto riesgo"
    # },
    # {
    #     "idDiagnostico": 103,
    #     "fechaRegistro": "2024-08-10",
    #     "Genero": "Masculino",
    #     "Edad": "60",
    #     "Hipertension": "Sí",
    #     "Cardiopatia": "Sí",
    #     "TipoTrabajo": "Oficina",
    #     "Nivel_GlucosaPromedio": "130",
    #     "ICM": "30.0",
    #     "EstadoFumador": "Sí",
    #     "Prediccion": "Moderado riesgo"
    # },
    # {
    #     "idDiagnostico": 104,
    #     "fechaRegistro": "2024-08-15",
    #     "Genero": "Femenino",
    #     "Edad": "55",
    #     "Hipertension": "No",
    #     "Cardiopatia": "No",
    #     "TipoTrabajo": "Hogar",
    #     "Nivel_GlucosaPromedio": "115",
    #     "ICM": "25.0",
    #     "EstadoFumador": "No",
    #     "Prediccion": "Bajo riesgo"
    # },
    # {
    #     "idDiagnostico": 105,
    #     "fechaRegistro": "2024-08-20",
    #     "Genero": "Masculino",
    #     "Edad": "65",
    #     "Hipertension": "Sí",
    #     "Cardiopatia": "Sí",
    #     "TipoTrabajo": "Campo",
    #     "Nivel_GlucosaPromedio": "140",
    #     "ICM": "32.5",
    #     "EstadoFumador": "Sí",
    #     "Prediccion": "Alto riesgo"
    # }
    # ]


    col_titulo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Registro de sus Diagnósticos", color=color, size=20, text_align="center")
            ]
        ),
        width=300,
        margin=20,
        alignment=ft.alignment.center,
    )

    tiles = []
    for index,registro in enumerate(registros):
        hipertension_text = "No presenta" if registro.get('Hipertension') == 0 else "Presenta"
        cardiopatia_text = "No presenta" if registro.get('Cardiopatia') == 0 else "Presenta"
        prediccion_text = "Presenta BAJO nivel de riesgo de ACV" if registro.get('prediccion') == 0 else "Presenta ALTO nivel de riesgo de ACV"
        tile = ft.ExpansionTile(
            title=ft.Text(f"Diagnóstico N° {index+1}       {registro['fechaRegistro']}", color=color_primary, size=17, font_family="LTSaeada-3"),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            #bgcolor=desplegable_diagnostico,
            bgcolor=ft.colors.TRANSPARENT,
            controls=[
                ft.ListTile(title=ft.Text(f"Hipertensión: {hipertension_text}", color=color, size=14), height=50),
                ft.ListTile(title=ft.Text(f"Cardiopatía: {cardiopatia_text}", color=color, size=14), height=50),
                ft.ListTile(title=ft.Text(f"Tipo de Trabajo: {registro['TipoTrabajo']}", color=color, size=14), height=50),
                ft.ListTile(title=ft.Text(f"Nivel de Glucosa Promedio: {registro['Nivel_GlucosaPromedio']}", color=color, size=14), height=50),
                ft.ListTile(title=ft.Text(f"ICM: {registro['ICM']}", color=color, size=14), height=50),
                ft.ListTile(title=ft.Text(f"Estado Fumador: {registro['EstadoFumador']}", color=color, size=14), height=50),
                ft.ListTile(title=ft.Text(f"Predicción: {prediccion_text}", color=color, size=14), height=50),
            ]
        )
        contenedor=ft.Container(
             content=tile,
             border_radius=10,
             border=ft.border.all(color=color_hint),
             padding=10,
             bgcolor=desplegable_diagnostico

             )
        tiles.append(contenedor)

    list_data = ft.Container(
        content=ft.Column(controls=tiles),
        width=300,
        margin=20
    )

    btn_estadistica = ft.TextButton(
        on_click=lambda e: view_chart(e, page, app_state),
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Estadísticas")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_primary,
            overlay_color=color_hovered,
        )
    )

    btn_hipertension = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Hipertensión")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_primary,
            overlay_color=color_hovered,
        )
    )

    btn_cardiopatia = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Cardiopatía")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_primary,
            overlay_color=color_hovered,
        )
    )

    btn_glucosa = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Glucosa")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_primary,
            overlay_color=color_hovered,
        )
    )

    btn_imc = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("IMC")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_primary,
            overlay_color=color_hovered,
        )
    )

    btn_predicción = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Predicción")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_primary,
            overlay_color=color_hovered,
        )
    )

    row_estadistica = ft.Container(
        content=ft.Row([btn_estadistica], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.only(bottom=20),
        width=300
    )

    row_buttons = ft.Container(
        content=ft.Row([btn_hipertension, btn_cardiopatia, btn_glucosa, btn_imc, btn_predicción], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS),
        padding=20,
        width=300
    )

    list_buttons = ft.ListView(
        controls=[row_estadistica]
    )

    list_data_scrollable = ft.ListView(
        controls=[list_data],
        expand=True
    )

    page.controls.append(col_titulo)
    page.controls.append(list_buttons)
    page.controls.append(list_data_scrollable)
    page.update()