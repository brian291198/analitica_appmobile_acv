import flet as ft
from flet import *
import requests
from login import login_view
from datetime import datetime
from styles import color, color_hint, color_primary, color_secondary, color_hovered, desplegable_diagnostico
from menubar import menubar
from urlsapi import DATA_OBJ_1

def view_chart(page, app_state):
    page.padding = 0

    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
        page.controls.clear()
        login_view(page, app_state)
        page.update()
        return
    
    # Obtener token
    token = app_state.token
    API_URL = DATA_OBJ_1

    registros = []

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
        

    # Extraer los últimos 6 registros
    registros = registros[-6:]

    # Ordenar los registros por fecha
    registros.sort(key=lambda x: datetime.strptime(x["fechaRegistro"], "%Y-%m-%d"))


    # Diccionario para traducir los nombres de los meses al español
    meses_espanol = {
        "Jan": "ENE", "Feb": "FEB", "Mar": "MAR", "Apr": "ABR", "May": "MAY", "Jun": "JUN",
        "Jul": "JUL", "Aug": "AGO", "Sep": "SEP", "Oct": "OCT", "Nov": "NOV", "Dec": "DIC"
    }

    def convertir_a_formato_personalizado(fecha_str):
        # Convertir la cadena de fecha a un objeto datetime
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        # Formatear la fecha en el formato "13\nSEP\n2024"
        dia = fecha.strftime("%d")
        mes = fecha.strftime("%b")
        anio = fecha.strftime("%Y")
        # Traducir el mes al español
        mes_espanol = meses_espanol[mes]
        return f"{dia}\n{mes_espanol}\n{anio}"

    # Eliminar duplicados (mismo fecha o glucosa)
    seen = set()
    registros_unicos = []
    for r in registros:
        fecha = r["fechaRegistro"]
        glucosa = r["Nivel_GlucosaPromedio"]
        if (fecha, glucosa) not in seen:
            seen.add((fecha, glucosa))
            registros_unicos.append(r)

    # Extraer fechas y niveles de glucosa únicos
    fechas = sorted(set(r["fechaRegistro"] for r in registros_unicos))
    niveles_glucosa = sorted(set(float(r["Nivel_GlucosaPromedio"]) for r in registros_unicos))

    # Extraer todas las fechas y niveles de glucosa hasta repetidos
    fechas_2 = [r["fechaRegistro"] for r in registros]
    niveles_glucosa_2 = [float(r["Nivel_GlucosaPromedio"]) for r in registros]

    # Convertir fechas en valores numéricos (índices)
    def fecha_a_numero(fecha):
        return fechas.index(fecha) + 1
    
    # Convertir niveles de glucosa en valores numéricos (índices)
    def glucosa_a_numero(glucosa):
        return niveles_glucosa.index(float(glucosa)) + 1

    # Crear los puntos de datos para el gráfico
    data_points = []
    for r in registros_unicos:
        fecha = fecha_a_numero(r["fechaRegistro"])
        glucosa = glucosa_a_numero(r["Nivel_GlucosaPromedio"])
        glucosa_tooltip = float(r["Nivel_GlucosaPromedio"])
        data_points.append(ft.LineChartDataPoint(fecha, glucosa, tooltip=f"Glucosa:\n{glucosa_tooltip}"))

    # Crear las etiquetas del eje Y
    data_left = [
        ft.ChartAxisLabel(
            value=i,
            label=ft.Text(str(nivel), size=10, color=ft.colors.with_opacity(1, color_primary)),
        )
        for i, nivel in enumerate(niveles_glucosa, start=1)
    ]

    # Crear las etiquetas del eje X (fechas)
    data_bottom = [
        ft.ChartAxisLabel(
            value=i + 1,
            label=ft.Container(
                ft.Text(convertir_a_formato_personalizado(fecha), size=10, color=ft.colors.with_opacity(1, color_primary)),
                margin=ft.margin.only(top=10, right=5),
            ),
        )
        for i, fecha in enumerate(fechas)
    ]

    # Configuración del gráfico
    chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=data_points,
                stroke_width=3,
                color=color_primary,
                curved=True,
                stroke_cap_round=True,
            )
        ],
        border=ft.border.all(3, ft.colors.with_opacity(1, color_secondary)),
        horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.colors.with_opacity(1, color_secondary), width=1),
        vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.colors.with_opacity(1, color_secondary), width=1),
        left_axis=ft.ChartAxis(labels=data_left, labels_size=40),
        bottom_axis=ft.ChartAxis(labels=data_bottom, labels_size=50),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
        min_y=1,
        max_y=len(niveles_glucosa),
        min_x=1,
        max_x=len(fechas),
        height=250,
    )

    comentario = "En la última fecha se visualiza un valor {} al anterior, lo que significa que se ha {} el nivel de glucosa, {}."
    if len(niveles_glucosa_2) > 1 and niveles_glucosa_2[-1] < niveles_glucosa_2[-2]:
        comentario = comentario.format("MENOR", "reducido", "¡sigue cuidando de tu salud!")
    else:
        comentario = comentario.format("MAYOR", "incrementado", "¡CUIDADO!")

    subtitulo_chart = ft.Text('Tendencia de variable "NIVEL DE GLUCOSA":', size=14, weight=ft.FontWeight.BOLD, color=color, text_align="center")
    row_subtitulo_chart = ft.Container(content=ft.Row([subtitulo_chart]), margin=ft.margin.only(top=20, bottom=20))

    # Configuración de interfaz
    texto_volver = ft.TextButton(
        on_click=lambda e: view_data(e, page, app_state),
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.ARROW_BACK_IOS_SHARP, color=ft.colors.WHITE, size=10),
                ft.Container(width=5),
                ft.Text("Volver", color=ft.colors.WHITE)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
    )

    col_superior = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=ft.Row([texto_volver], alignment=ft.MainAxisAlignment.END), margin=ft.margin.only(right=5)),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=color_primary,
        padding=ft.padding.only(left=20, top=10, bottom=10, right=20),
    )

    principal_container = ft.Container(
        content=ft.Column([col_superior]),
        width=1000
    )
    
    col_chart = ft.Container(
        content=ft.Column(
            controls=[
                row_subtitulo_chart,
                chart,
                ft.Text(comentario, size=14, color=color),
                ft.Container(height=500, bgcolor=ft.colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.ALWAYS
        ),
        padding=15,
        margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
        border=ft.border.all(color=color_hint),
        border_radius=10,
    )

    chart_scrollable = ft.ListView(controls=[col_chart], expand=True)
    titulo_chart = ft.Text("Seguimiento y Monitoreo de \nVariables de Predicción", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align="center")
    row_titulo_chart = ft.Container(content=ft.Row([titulo_chart], alignment=ft.MainAxisAlignment.CENTER), bgcolor=color_primary, padding=ft.padding.only(top=5, bottom=20), margin=ft.margin.only(top=-1))

    page.controls.append(principal_container)
    page.controls.append(row_titulo_chart)
    page.controls.append(chart_scrollable)
    page.update()

def view_data(e, page, app_state):
    page.controls.clear()
    menu_bar = menubar(page, app_state)
    page.controls.append(menu_bar)
    page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
    app_state.show_data_diagnostico()
    page.update()