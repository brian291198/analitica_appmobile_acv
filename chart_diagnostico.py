import flet as ft
from flet import *
import requests
from login import login_view
from datetime import datetime
from styles import color, color_hint, color_primary, color_secondary, color_hovered, desplegable_diagnostico, color_check, color_error
from menubar import menubar
from urlsapi import DATA_OBJ_1

chart_scrollable = None

def view_chart(page, app_state):

    global chart_scrollable


    chart_scrollable=ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(src=f"/estadisticas.png", width=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.FIT_HEIGHT),
                ft.Text("Seleccione una opción\npara visualizar", color=color, size=12, text_align="center"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        height=500, 
        margin=ft.margin.only(top=50, bottom=20), 
        bgcolor=ft.colors.WHITE, 
        padding=ft.padding.only(top=5, bottom=20), 
        
        )

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


    # Extraer datos únicos
    fechas = sorted(set(r["fechaRegistro"] for r in registros_unicos))
    niveles_glucosa = sorted(set(float(r["Nivel_GlucosaPromedio"]) for r in registros_unicos))
    niveles_imc = sorted(set(float(r["ICM"]) for r in registros_unicos))
    niveles_trabajo = sorted(set(str(r["TipoTrabajo"]) for r in registros_unicos))
    niveles_fumador = sorted(set(str(r["EstadoFumador"]) for r in registros_unicos))


    # Extraer todos los datos hasta repetidos
    fechas_2 = [r["fechaRegistro"] for r in registros]
    niveles_glucosa_2 = [float(r["Nivel_GlucosaPromedio"]) for r in registros]
    niveles_imc_2 = [float(r["ICM"]) for r in registros]
    niveles_trabajo_2 = [str(r["TipoTrabajo"]) for r in registros]
    niveles_fumador_2 = [str(r["EstadoFumador"]) for r in registros]

    print(niveles_trabajo_2[-1])

    # Convertir fechas en valores numéricos (índices)
    def fecha_a_numero(fecha):
        return fechas.index(fecha) + 1
    
    # Convertir niveles de glucosa en valores numéricos (índices)
    def glucosa_a_numero(glucosa):
        return niveles_glucosa.index(float(glucosa)) + 1
    
    # Convertir niveles de imc en valores numéricos (índices)
    def imc_a_numero(imc):
        return niveles_imc.index(float(imc)) + 1
    
    # Convertir tipotrabajo en valores numéricos (índices)
    def trabajo_a_numero(trabajo):
        return niveles_trabajo.index(str(trabajo)) + 1
    
    # Convertir fumador en valores numéricos (índices)
    def fumador_a_numero(fumador):
        return niveles_fumador.index(str(fumador)) + 1

    # Crear los puntos de datos para el gráfico de GLUCOSA VS FECHA
    data_points = []
    for r in registros_unicos:
        fecha = fecha_a_numero(r["fechaRegistro"])
        glucosa = glucosa_a_numero(r["Nivel_GlucosaPromedio"])
        glucosa_tooltip = float(r["Nivel_GlucosaPromedio"])
        data_points.append(ft.LineChartDataPoint(fecha, glucosa, tooltip=f"Glucosa:\n{glucosa_tooltip}"))

    # Crear los puntos de datos para el gráfico de IMC VS FECHA
    data_points_imc = []
    for r in registros_unicos:
        fecha = fecha_a_numero(r["fechaRegistro"])
        imc = imc_a_numero(r["ICM"])
        imc_tooltip = float(r["ICM"])
        data_points_imc.append(ft.LineChartDataPoint(fecha, imc, tooltip=f"IMC:\n{imc_tooltip}"))
    
    # Crear los puntos de datos para el gráfico de trabajo VS FECHA
    data_points_trabajo = []
    for r in registros_unicos:
        fecha = fecha_a_numero(r["fechaRegistro"])
        trabajo = trabajo_a_numero(r["TipoTrabajo"])
        trabajo_tooltip = str(r["TipoTrabajo"])
        data_points_trabajo.append(ft.LineChartDataPoint(fecha, trabajo, tooltip=f"Tipo:\n{trabajo_tooltip}"))

     # Crear los puntos de datos para el gráfico de fumador VS FECHA
    data_points_fumador = []
    for r in registros_unicos:
        fecha = fecha_a_numero(r["fechaRegistro"])
        fumador = fumador_a_numero(r["EstadoFumador"])
        fumador_tooltip = str(r["EstadoFumador"])
        data_points_fumador.append(ft.LineChartDataPoint(fecha, fumador, tooltip=f"Estado:\n{fumador_tooltip}"))

    # Crear las etiquetas del eje Y GLUCOSA
    data_left = [
        ft.ChartAxisLabel(
            value=i,
            label=ft.Text(str(nivel), size=10, color=ft.colors.with_opacity(1, color_primary)),
        )
        for i, nivel in enumerate(niveles_glucosa, start=1)
    ]

    # Crear las etiquetas del eje Y IMC
    data_left_imc = [
        ft.ChartAxisLabel(
            value=i,
            label=ft.Text(str(nivel), size=10, color=ft.colors.with_opacity(1, color_primary)),
        )
        for i, nivel in enumerate(niveles_imc, start=1)
    ]

    # Crear las etiquetas del eje Y IMC
    data_left_trabajo = [
        ft.ChartAxisLabel(
            value=i,
            label=ft.Text(str(nivel), size=10, color=ft.colors.with_opacity(1, color_primary)),
        )
        for i, nivel in enumerate(niveles_trabajo, start=1)
    ]

    # Crear las etiquetas del eje Y IMC
    data_left_fumador = [
        ft.ChartAxisLabel(
            value=i,
            label=ft.Text(str(nivel), size=10, color=ft.colors.with_opacity(1, color_primary)),
        )
        for i, nivel in enumerate(niveles_fumador, start=1)
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
    def create_chart(data_points, data_left, data_bottom, max_y, max_x):
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
            max_y=len(max_y),
            min_x=1,
            max_x=len(max_x),
            height=250,
            width=500,
        )
        return chart
    
    def comment_text(valor, ident):
        comentario = "En la última fecha se visualiza un valor {} al anterior, lo que significa que se ha {} el nivel de {}, {}."
        if len(valor) > 1 and valor[-1] < valor[-2]:
            comentario = comentario.format("MENOR", "reducido", ident, "¡sigue cuidando de tu salud!")
            
        else:
            comentario = comentario.format("MAYOR", "incrementado", ident,  "¡CUIDADO!")
            
        return comentario

     
    def comment_valor_actual(valor, ident):

        if ident=="ESTADO FUMADOR":
            if valor[-1] == "No opina":
                comentario = ft.Text("Es crucial tener claridad sobre los hábitos de fumar, ya que la incertidumbre podría dificultar la evaluación del riesgo de ACV.", color=color)
            elif valor[-1] == "Anteriormente fumó":
                comentario = ft.Text("Aunque dejó de fumar, es importante considerar los años en los que se fumó, ya que pueden influir en el riesgo de ACV.", color=color)
            elif valor[-1] == "Nunca fumó":
                comentario = ft.Text("El no haber fumado es un factor positivo en la reducción del riesgo de ACV.", color=color)
            else:
                comentario = ft.Text("El hábito de fumar aumenta significativamente el riesgo de ACV. Considera estrategias para dejar de fumar.", color=color)
        else:
            if str(valor[-1])== "Trabajador para el gobierno":
                comentario = ft.Text("Como trabajador para el gobierno, es posible que enfrentes un nivel de estrés más bajo en comparación con otros sectores, lo cual puede influir positivamente en la salud cardiovascular. Mantén un equilibrio saludable entre el trabajo y el tiempo personal para minimizar el riesgo de ACV.", color=color)
            elif str(valor[-1])== "Nunca trabajó":
                comentario = ft.Text("No haber trabajado puede estar asociado a factores socioeconómicos que podrían influir en tu salud. Asegúrate de mantener una rutina saludable y realizar chequeos médicos regulares para monitorear tu riesgo de ACV.", color=color)
            elif str(valor[-1])== "Trabajador privado":
                comentario = ft.Text("Trabajar en el sector privado a menudo implica una mayor carga de estrés y horarios más largos, lo cual puede aumentar el riesgo de ACV. Considera técnicas de manejo del estrés y busca oportunidades para equilibrar tu carga laboral con actividades relajantes.", color=color)
            else:
                comentario = ft.Text("Como trabajador por cuenta propia, podrías experimentar altos niveles de estrés y responsabilidades que podrían afectar tu salud cardiovascular. Es importante gestionar el estrés de manera efectiva y llevar un estilo de vida saludable para reducir el riesgo de ACV.", color=color)
        return comentario
    
    def valor_actual(valor, ident):
        

        state_variable = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"{ident} Actual: ", size=14, color=color_hint),
                    ft.Text(valor[-1], size=14, color=color),
                ],
                horizontal_alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS
            ),
            padding=15,
            margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
            border=ft.border.all(color=color_hint),
            #bgcolor=ft.colors.GREEN_100,
            border_radius=10,
            )
      
        return state_variable
    
    def valor_actual_g_imc(valor, ident):

        if ident == "GLUCOSA":
            if valor[-1] >= 50 and valor[-1] < 70:
                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.RED_500),
                bgcolor=ft.colors.RED_100,
                border_radius=10,
                )
            elif valor[-1] >= 70 and valor[-1] <= 100:

                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.GREEN),
                bgcolor=ft.colors.GREEN_100,
                border_radius=10,
                )
            else:

                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.RED_500),
                bgcolor=ft.colors.RED_100,
                border_radius=10,
                )
        else:
            if valor[-1] < 17:
                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.RED_500),
                bgcolor=ft.colors.RED_100,
                border_radius=10,
                )  
            elif valor[-1] >= 17 and valor[-1] < 18.5:
                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.YELLOW_500),
                bgcolor=ft.colors.YELLOW_100,
                border_radius=10,
                )
            elif valor[-1] >= 18.5 and valor[-1] < 25:
                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.GREEN),
                bgcolor=ft.colors.GREEN_100,
                border_radius=10,
                )
            elif valor[-1] >= 25 and valor[-1] < 30:
                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.YELLOW_500),
                bgcolor=ft.colors.YELLOW_100,
                border_radius=10,
                )
            else:
                state_variable = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"Nivel de {ident} Actual: ", size=14, color=color),
                        ft.Text(valor[-1], size=14, color=color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=15,
                margin=ft.margin.only(left=15, right=15, top=20, bottom=15),
                border=ft.border.all(color=ft.colors.RED_500),
                bgcolor=ft.colors.RED_100,
                border_radius=10,
                )
        return state_variable
    
    def valor_actual_g_imc(valor, ident):

        if ident == "GLUCOSA":
            if valor[-1] < 50:
                comentario = ft.Text("Este nivel de glucosa, denominado Hipoglucemia Nivel 2, es extremadamente bajo y puede causar síntomas severos. Es fundamental actuar rápidamente para elevar los niveles de glucosa, ya que un nivel tan bajo puede aumentar significativamente el riesgo de un accidente cerebrovascular.", size=14, color=color),

            elif valor[-1] >= 50 and valor[-1] < 70:
                comentario = ft.Text("La Hipoglucemia Nivel 1 indica un nivel bajo de glucosa en sangre. Aunque menos crítico que el Nivel 2, sigue siendo importante tratar de elevar los niveles de glucosa para evitar complicaciones, como un mayor riesgo de accidente cerebrovascular.", size=14, color=color),

            elif valor[-1] >= 70 and valor[-1] <= 100:
                comentario = ft.Text("Este rango de glucosa, típico en pacientes sanos, se considera óptimo para mantener una buena salud general y reducir el riesgo de eventos cerebrovasculares. Mantenerse dentro de este rango es clave para prevenir complicaciones.", size=14, color=color),
            else:
                comentario = ft.Text("Para pacientes diabéticos, mantener la glucosa en sangre entre 70 y 130 mg/dL ayuda a gestionar su condición de manera efectiva y minimiza el riesgo de complicaciones como el accidente cerebrovascular. Es importante seguir las recomendaciones médicas para mantener los niveles dentro de este rango.", size=14, color=color),


        else:
            if valor[-1] < 17:
                comentario = ft.Text("Un IMC por debajo de 16.9, denominado Muy Bajo Peso, indica una posible desnutrición o problemas de salud graves. Es crucial consultar con un profesional médico para abordar posibles deficiencias nutricionales y prevenir riesgos de salud, como problemas cardiovasculares o metabólicos.", size=14, color=color),

            elif valor[-1] >= 17 and valor[-1] < 18.5:
                comentario = ft.Text("Un IMC en el rango de 17 a 18.4, clasificado como Bajo Peso, puede indicar una falta de masa corporal adecuada. Aunque no tan crítico como el Muy Bajo Peso, es importante considerar ajustes en la dieta y el estilo de vida para alcanzar un peso más saludable y reducir el riesgo de problemas metabólicos.", size=14, color=color),
            elif valor[-1] >= 18.5 and valor[-1] < 25:
                comentario = ft.Text("El rango de IMC de 18.5 a 24.9 es considerado Normal y refleja un peso saludable. Mantenerse dentro de este rango ayuda a reducir el riesgo de enfermedades crónicas, incluidos problemas cardiovasculares y diabetes, promoviendo una buena salud general.", size=14, color=color),
            elif valor[-1] >= 25 and valor[-1] < 30:
                comentario = ft.Text("Un IMC de 25 a 29.9, denominado Sobrepeso, sugiere un exceso de peso que podría incrementar el riesgo de condiciones como enfermedades cardíacas y diabetes tipo 2. Es recomendable adoptar un estilo de vida saludable, con una dieta equilibrada y actividad física regular, para reducir el riesgo asociado.", size=14, color=color),
            elif valor[-1] >= 30 and valor[-1] < 35:
                comentario = ft.Text("Un IMC de 30 a 34.9 indica Obesidad, una condición que aumenta significativamente el riesgo de enfermedades crónicas, como hipertensión y diabetes. Es crucial consultar con un profesional de la salud para desarrollar un plan de manejo del peso y minimizar riesgos asociados.", size=14, color=color),
            elif valor[-1] >= 35 and valor[-1] < 40:
                comentario = ft.Text("El rango de IMC de 35 a 39.9, conocido como Obesidad Marcada, representa un riesgo elevado de complicaciones de salud graves, incluyendo problemas cardiovasculares y respiratorios. Se recomienda una intervención médica intensiva para gestionar el peso y reducir riesgos.", size=14, color=color),
            else:
                comentario = ft.Text("Un IMC superior a 40 se clasifica como Obesidad Mórbida y está asociado con un alto riesgo de problemas de salud graves, como enfermedades cardiovasculares y metabólicas. Es vital buscar asesoramiento médico para un plan de tratamiento y manejo integral del peso para mejorar la salud y calidad de vida.", size=14, color=color),
        return comentario
    
    
    
    
    def report_stadistic(e, ident, page, chart_scrollable_container, data_points, data_left, data_bottom, variable_1, variable_2, fechas, message):
        global chart_scrollable 
        if ident == "GLUCOSA":
            btn_glucosa.disabled=True
            btn_glucosa.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_primary},
            )
            btn_imc.disabled=False
            btn_imc.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_fumador.disabled=False
            btn_fumador.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_trabajo.disabled=False
            btn_trabajo.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
        else:
            btn_glucosa.disabled=False
            btn_glucosa.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_imc.disabled=True
            btn_imc.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_primary},
            )
            btn_fumador.disabled=False
            btn_fumador.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_trabajo.disabled=False
            btn_trabajo.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
        

        
        subtitulo_chart = ft.Text(f'Tendencia de variable "NIVEL DE {ident}":', size=14, weight=ft.FontWeight.BOLD, color=color, text_align="center")
        row_subtitulo_chart = ft.Container(content=ft.Row([subtitulo_chart]), margin=ft.margin.only(top=20, bottom=20))

        
        #CONTENEDOR PARA GRÁFICO DE LINEAS
        col_chart = ft.Container(
            content=ft.Column(
                controls=[
                    row_subtitulo_chart,
                    create_chart(data_points, data_left, data_bottom, variable_1, fechas),
                    ft.Container(height=20),
                    ft.Text(comment_text(variable_2, ident), size=14, color=color),
                    valor_actual_g_imc(variable_2, ident),
                    ft.Text(message, size=14, color=color),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS
            ),
            padding=15,
            margin=ft.margin.only(left=15, right=15, top=20, bottom=20),
            border=ft.border.all(color=color_hint),
            border_radius=10,
        )

        if chart_scrollable in page.controls:
            page.controls.remove(chart_scrollable)
        page.update()
        chart_scrollable = ft.ListView(controls=[col_chart], expand=True)
        page.controls.append(chart_scrollable)
        page.update()
    
    def report_stadistic_2(e, ident, page, chart_scrollable_container, data_points, data_left, data_bottom, variable_1, variable_2, fechas, message):
        global chart_scrollable 

        if ident == "ESTADO FUMADOR":
            btn_glucosa.disabled=False
            btn_glucosa.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_imc.disabled=False
            btn_imc.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_fumador.disabled=True
            btn_fumador.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_primary},
            )
            btn_trabajo.disabled=False
            btn_trabajo.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
        else:
            btn_glucosa.disabled=False
            btn_glucosa.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_imc.disabled=False
            btn_imc.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_fumador.disabled=False
            btn_fumador.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_hint},
            )
            btn_trabajo.disabled=True
            btn_trabajo.style = ft.ButtonStyle(
            color={"": ft.colors.WHITE},
            bgcolor={"": color_primary},
            )
        
        subtitulo_chart = ft.Text(f'Tendencia de variable "{ident}":', size=14, weight=ft.FontWeight.BOLD, color=color, text_align="center")
        row_subtitulo_chart = ft.Container(content=ft.Row([subtitulo_chart]), margin=ft.margin.only(top=20, bottom=20))

        
        #CONTENEDOR PARA GRÁFICO DE LINEAS
        col_chart = ft.Container(
            content=ft.Column(
                controls=[
                    row_subtitulo_chart,
                    create_chart(data_points, data_left, data_bottom, variable_1, fechas),
                    ft.Container(height=20),
                    comment_valor_actual(variable_2, ident),
                    valor_actual(variable_2, ident)
                    #ft.Text(message, size=14, color=color),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS
            ),
            padding=15,
            margin=ft.margin.only(left=15, right=15, top=20, bottom=20),
            border=ft.border.all(color=color_hint),
            border_radius=10,
        )

        if chart_scrollable in page.controls:
            page.controls.remove(chart_scrollable)
        page.update()
        chart_scrollable = ft.ListView(controls=[col_chart], expand=True)
        page.controls.append(chart_scrollable)
        page.update()



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
            width=2000
        )

    #BOTONES PARA CADA GRÁFICO

    btn_trabajo = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Tipo Trabajo")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_hint,
            overlay_color=color_hovered,
        ),
        on_click=lambda e: report_stadistic_2(e, "TIPO DE TRABAJO", page, chart_scrollable, data_points_trabajo, data_left_trabajo, data_bottom, niveles_trabajo, niveles_trabajo_2, fechas, " ")
    )

    btn_fumador = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.AREA_CHART, color=ft.colors.WHITE, size=20),
                ft.Text("Estado Fumador")
            ]
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color_hint,
            overlay_color=color_hovered,
        ),
        on_click=lambda e: report_stadistic_2(e, "ESTADO FUMADOR", page, chart_scrollable, data_points_fumador, data_left_fumador, data_bottom, niveles_fumador, niveles_fumador_2, fechas, " ")
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
            bgcolor=color_hint,
            overlay_color=color_hovered,
        ),
        on_click=lambda e: report_stadistic(e, "GLUCOSA", page, chart_scrollable, data_points, data_left, data_bottom, niveles_glucosa, niveles_glucosa_2, fechas, "• Hipoglucemia Nivel 2: glucosa en sangre inferior a 53 mg/dL.\n• Hipoglucemia Nivel 1: glucosa en sangre inferior a 70 mg/dL.\n• Pacientes sanos: rango de 70-100 mg/dL.\n• Pacientes diabéticos: rango de 70-130 mg/dL.")
        #on_click = lambda e: prueba(e, page, chart_scrollable)
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
            bgcolor=color_hint,
            overlay_color=color_hovered,
        ),
        on_click=lambda e: report_stadistic(e, "IMC", page, chart_scrollable, data_points_imc, data_left_imc, data_bottom, niveles_imc, niveles_imc_2, fechas, "• Muy Bajo Peso: IMC menor a 16.9\n• Bajo Peso: IMC de 17 a 18.4\n• Normal: IMC de 18.5 a 24.9\n• Sobrepeso: IMC de 25 a 29.9\n• Obesidad: IMC de 30 a 34.9\n• Obesidad Marcada: IMC de 35 a 39.9\n• Obesidad Mórbida: IMC mayor a 40")
    )

    row_buttons = ft.Container(
        content=ft.Row([btn_glucosa, btn_imc, btn_trabajo, btn_fumador, ], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.HIDDEN), #cambiar a HIDDEN
        padding=ft.padding.only(top=20, bottom=20,right=15, left=15),
        width=2000
    )

    list_buttons = ft.ListView(
        controls=[row_buttons]
    )

    titulo_chart = ft.Text("Seguimiento y Monitoreo de \nVariables de Predicción", size=18, color=ft.colors.WHITE, text_align="center")
    row_titulo_chart = ft.Container(content=ft.Row([titulo_chart], alignment=ft.MainAxisAlignment.CENTER), bgcolor=color_primary, padding=ft.padding.only(top=5, bottom=20), margin=ft.margin.only(top=-1))
   
    page.controls.append(principal_container)
    page.controls.append(row_titulo_chart)
    page.controls.append(list_buttons)
    page.controls.append(chart_scrollable)
    page.update()

def view_data(e, page, app_state):

    page.controls.clear()
    menu_bar = menubar(page, app_state)
    page.controls.append(menu_bar)
    page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
    app_state.show_data_diagnostico()
    page.update()