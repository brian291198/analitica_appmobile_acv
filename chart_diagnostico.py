import flet as ft
from flet import *
import requests
from login import login_view
from datetime import datetime
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered, desplegable_diagnostico
from menubar import menubar

def view_chart(page, app_state):

    page.padding=0

    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return
    
    def view_data(e, page, app_state):
            page.controls.clear()
            menu_bar=menubar(page, app_state)
            page.controls.append(menu_bar)
            page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
            app_state.show_data_diagnostico()
            page.update()


    #ELEMENTOS------------------------------------------------------------------------------------------------------------------------------------
    #boton en texto -> < VOLVER
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

    #CONTAINERS PARA SEPARAR COLUMNAS DE ELEMENTOS-----------------------------------------------------------------------------------------------------
    col_volver=ft.Container(content=ft.Row([
                texto_volver
            ], alignment=ft.MainAxisAlignment.END
            ),
            #width=360,
            margin=ft.margin.only(right=5), 
            )
    #----------------------------------------------------------------------------------------------------------------------------------------------  
    #CONTAINERS PARA SEPARAR FILAS DE ELEMENTOS


    col_superior=ft.Container(content=ft.Column([
                col_volver,
                #row_titulo_container,              
        ],spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ), 
        bgcolor=color_primary,
        padding=ft.padding.only(left=20, top=10, bottom=10, right=20), #corregir bottom=20
        )
    
    row_superior=ft.Container(content=ft.Column([
                col_superior,
                #row_form
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
        ), 
        alignment=ft.alignment.center,
        #border=ft.border.all(),

        )
    
    principal_container=ft.Container(content=ft.Column([
                row_superior,
        ],),width=1000
        )


    #page.controls.clear()
    page.controls.append(principal_container)
    page.update()


     #GRÁFICO ESTADÍSTICO------------------------------------------------------------------------------------------------------------------------------------
    
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

    # Extraer datos para el gráfico
    fechas = [r["fechaRegistro"] for r in registros]
    niveles_glucosa = [int(r["Nivel_GlucosaPromedio"]) for r in registros]
    max_glucosa = max(niveles_glucosa)

    # Crear los puntos de datos para el gráfico
    data_points = [
        ft.LineChartDataPoint(x, y)
        for x, y in enumerate(niveles_glucosa, start=1)
    ]

    left_items=[]

    for i in range(25, max_glucosa + 1, 10):
            left=ft.ChartAxisLabel(
                value=i,
                label=ft.Text(f"{str(i)}", color="#333333", size=10, weight=ft.FontWeight.BOLD),
            ) 
            #print(f"{str(i)}")
            left_items.append(left)
          

    # Configurar el gráfico
    """ chart = ft.LineChart(
    data_series=[
        ft.LineChartData(
            data_points=data_points,
            stroke_width=3,
            color=ft.colors.LIGHT_GREEN,
        ),
    ],
    min_y=25,
    max_y=max_glucosa,
    min_x=1,
    max_x=len(fechas),
    border=ft.border.all(),
    left_axis=ft.ChartAxis(
        labels=left_items,
        labels_size=10,
    ),
    bottom_axis=ft.ChartAxis(
        labels=[
            ft.ChartAxisLabel(
                value=i+1,
                label=ft.Text(
                    fecha,
                    color="#333333",  # Color del texto de los valores del eje X
                )
            ) for i, fecha in enumerate(fechas)
        ],
        labels_size=12,
    ),
    width=300,
    height=500,
) """

    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, 3),
                ft.LineChartDataPoint(2.6, 2),
                ft.LineChartDataPoint(4.9, 5),
                ft.LineChartDataPoint(6.8, 3.1),
                ft.LineChartDataPoint(8, 4),
                ft.LineChartDataPoint(9.5, 3),
                ft.LineChartDataPoint(11, 4),
            ],
            stroke_width=3,
            color=color_primary,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    chart = ft.LineChart(
        data_series=data_1,
        border=ft.border.all(3, ft.colors.with_opacity(1, color_secondary)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(1, color_secondary), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(1, color_secondary), width=1
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Text("10K", size=14,color=ft.colors.with_opacity(1, color_primary)),
                ),
                ft.ChartAxisLabel(
                    value=3,
                    label=ft.Text("30K", size=14, color=ft.colors.with_opacity(1, color_primary)),
                ),
                ft.ChartAxisLabel(
                    value=5,
                    label=ft.Text("50K", size=14, color=ft.colors.with_opacity(1, color_primary)),
                ),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text(
                            "MAR",
                            size=16,
                            #weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(1, color_primary),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=5,
                    label=ft.Container(
                        ft.Text(
                            "JUN",
                            size=16,
                            #weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(1, color_primary),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=8,
                    label=ft.Container(
                        ft.Text(
                            "SEP",
                            size=16,
                            #weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(1, color_primary),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
        min_y=0,
        max_y=6,
        min_x=0,
        max_x=11,
        # animate=5000,
        height=200,
    )


    # Determinar el comentario basado en los valores de glucosa
    if niveles_glucosa[-1] < niveles_glucosa[-2]:
        comentario = "En la última fecha se visualiza un valor MENOR al anterior, lo que significa que ha reducido el nivel de hipertensión, lo cual implica una reducción del riesgo a padecer un accidente cerebrovascular, ánimo sigue cuidando de tu salud!"
    else:
        comentario = "En la última fecha se visualiza un valor MAYOR al anterior, lo que significa que ha incrementado el nivel de hipertensión, ¡CUIDADO! \nEso implica un aumento del riesgo a padecer un accidente cerebrovascular, cuida tu salud!."
    
    subtitulo_chart=ft.Text('Tendencia de variable "HIPERTENSIÓN":', size=14,weight=ft.FontWeight.BOLD, color=color, text_align="center")
    
    row_subtitulo_chart=ft.Container(content=Row([
          subtitulo_chart,
    ],),margin=ft.margin.only(top=20, bottom=20))


    col_chart=ft.Container(content=ft.Column(controls=[
            row_subtitulo_chart,
            chart,
            ft.Text(comentario, size=14, color=color),
            ft.Container(height=500,width=360, bgcolor=ft.colors.WHITE),
        ],alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS),padding=20, margin=10,width=300)


    chart_scrollable = ft.ListView(
        controls=[col_chart],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
        )
    
    titulo_chart=ft.Text("Estadísticas de \nVariables de Predicción", size=18,weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align="center")

    row_titulo_chart=ft.Container(content=ft.Row([
          titulo_chart,
    ],alignment=ft.MainAxisAlignment.CENTER),bgcolor=color_primary,padding=ft.padding.only(top=5, bottom=30), margin=ft.margin.only(top=-1))

    #page.controls.clear()
    page.controls.append(row_titulo_chart)
    page.controls.append(chart_scrollable)
    page.update()
