import flet as ft
import requests
import asyncio
from login import login_view
from api_whatsapp import message_whatsapp
from datetime import datetime
from validation import validate_dropdown, validate_intervalo
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_check, color_error
from menubar import menubar
from urlsapi import HTTP_OBJ_1, HTTP_GRUPO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
from flet.matplotlib_chart import MatplotlibChart


def obtener_grupos_api(grupo_seleccionado, token):
    """Función para obtener datos de la API según el grupo seleccionado."""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    params = {
        'grupo': grupo_seleccionado,  
    }
    response = requests.get(f'{HTTP_GRUPO}', headers=headers, params=params)
    if response.status_code == 200:
        datos = response.json().get('grupos', [])
        marcas = response.json().get('marcas', [])
        generos = response.json().get('generos', [])
        tallas = response.json().get('tallas', [])
        colores = response.json().get('colores', [])
        productos = response.json().get('productos', [])
        return datos, marcas, generos, tallas, colores, productos
    else:
        print("Error al obtener datos:", response.text)
        return [], [], [], [], [], []
    
def actualizar_combos(seleccion_grupo, ip_marca, ip_genero, ip_talla, ip_color,ip_producto, token):
    bandera, nuevos_datos, generos, tallas, colores, productos = obtener_grupos_api(seleccion_grupo, token)
    nuevos_datos = ['TODOS'] + nuevos_datos
    ip_marca.options = [ft.dropdown.Option(dato) for dato in nuevos_datos] 
    ip_marca.update()
    generos = ['TODOS'] + generos
    ip_genero.options = [ft.dropdown.Option(genero) for genero in generos] 
    ip_genero.update()
    tallas = ['TODOS'] + tallas
    ip_talla.options = [ft.dropdown.Option(talla) for talla in tallas] 
    ip_talla.update() 
    colores = ['TODOS'] + colores
    ip_color.options = [ft.dropdown.Option(color) for color in colores] 
    ip_color.update()
    productos = ['TODOS'] + productos
    ip_producto.options = [ft.dropdown.Option(producto) for producto in productos] 
    ip_producto.update()

#VISTA DE PREDICCIÓN DE DEMANDA - OBJETIVO 1
def objetive1_view(page, app_state):
        page.padding=0

        if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return
        #Obtener token
        token =app_state.token

        opciones, opciones_marca, generos, tallas, colores, productos = obtener_grupos_api(None,token)

        global prediccion_resultado 
        global tabla_predicciones  
        API_URL = HTTP_OBJ_1
        
        #----------------------------------------------------------------------------------------------------------------------------------------------
        #MÉTODOS

        # error_genero = ""

        # def validar_inputs(e):
        #     nonlocal error_genero

        #     # Validación del género
        #     if ip_genero.value == "" or None:
        #         error_genero = "Por favor, seleccione un género válido."
        #     else:
        #         error_genero = ""  # Limpia el mensaje si la validación es correcta

        #     # Actualiza el mensaje de error en la interfaz
        #     txt_error_genero.value = error_genero
        #     txt_error_genero.update()

        def accion_volver_home(e, page, app_state):
            page.controls.clear()
            menu_bar=menubar(page, app_state)
            page.controls.append(menu_bar)
            page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
            app_state.show_home()
            page.update()
        
        def seleccionado(e, col_control):
            value=e.control.value
            if value:
                col_control.border=ft.border.all(color=ft.colors.BLUE_400, width=1)
                page.update()
                # Espera breve para volver al borde normal
                time.sleep(0.4)
                col_control.border = ft.border.all(color=color_hint, width=1)
                page.update()
            else:
                return None

        def diagnosticar(e):
            # Recoger los valores de los campos del formulario
            datos = {
                "Tienda": ip_tienda.value if ip_tienda.value and ip_tienda.value != "TODOS" else None,
                "Marca": ip_marca.value if ip_marca.value and ip_marca.value != "TODOS" else None,
                "Grupo": ip_grupos.value if ip_grupos.value and ip_grupos.value != "TODOS" else None,
                "Genero": ip_genero.value if ip_genero.value and ip_genero.value != "TODOS" else None,
                "TALLA": ip_talla.value if ip_talla.value and ip_talla.value != "TODOS" else None,
                "COLOR": ip_color.value if ip_color.value and ip_color.value != "TODOS" else None,
                "Descripcion Producto": ip_producto.value if ip_producto.value and ip_producto.value != "TODOS" else None
            }
            
            datos_values = [value for key, value in datos.items()]
            datos_keys = [key for key in datos.keys()]

            # Lista para errores
            errores = []

            #Aspecto de carga
            loading = ft.AlertDialog(
                    #title=ft.Text("Error", color=ft.colors.RED),
                    #content=ft.Text(list_errores, color=ft.colors.RED),
                    content=ft.Container(
                                width=page.width,
                                height=page.height,
                                alignment=ft.alignment.center,  # Centrar el contenido (el indicador de carga)
                                content=ft.CupertinoActivityIndicator(
                                    radius=20,
                                    color=ft.colors.WHITE,
                                    animating=True,
                                ),
                                visible=True,  # Inicia oculto
                            ),
                    bgcolor=ft.colors.TRANSPARENT,
                    shape=ft.RoundedRectangleBorder(10)
                )
            page.open(loading)
            time.sleep(0.5)
            page.close(loading)
            page.update()
            
            # Imprimir errores
            list_errores="\n".join(errores)

            if errores:
                alert_error = ft.AlertDialog(
                    title=ft.Text("Error", color=ft.colors.RED),
                    content=ft.Text(list_errores, color=ft.colors.RED),
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(10)
                )
                page.open(alert_error)
                print(datos)

            else: 
                    # Definir las cabeceras para la solicitud
                    headers = {
                        'Authorization': f'Token {token}',
                        'Content-Type': 'application/json'
                    }

                    # Enviar una solicitud POST a la API
                    try:    
                        response = requests.post(API_URL, json=datos, headers=headers)

                        if response.status_code == 200:
                            # Crear un contenedor de alerta de aprobación
                            aprobado = ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.CHECK_CIRCLE_ROUNDED, color=color_check, size=30),
                                        ft.Text("Predicción Realizada", color=color, size=14)
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            )
                            
                            # Crear una alerta con la aprobación
                            alert_aprobado = ft.AlertDialog(
                                content=aprobado,
                                bgcolor=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(10),
                            )
                            
                            # Mostrar y luego cerrar la alerta
                            page.open(alert_aprobado)
                            time.sleep(1.5)
                            page.close(alert_aprobado)

                            # Obtener el JSON de respuesta
                            response_json = response.json()
                            predicciones = response_json.get('predicciones', [])
                            print(predicciones)



                            # Inicializar una lista para almacenar las filas de la tabla
                            filas_tabla = []

                            if predicciones:
                                print(predicciones)
                                meses = []
                                cantidades = []

                                tienda = response_json.get('tienda')
                                tienda = tienda if tienda is not None else 'N/A'

                                marca = response_json.get('marca')
                                marca = marca if marca is not None else 'N/A'

                                grupo = response_json.get('grupo')
                                grupo = grupo if grupo is not None else 'N/A'

                                genero = response_json.get('genero')
                                genero = genero if genero is not None else 'N/A'

                                talla = response_json.get('talla')
                                talla = talla if talla is not None else 'N/A'

                                c_olor = response_json.get('color')
                                c_olor = c_olor if c_olor is not None else 'N/A'

                                producto = response_json.get('descripcion')
                                producto = producto if producto is not None else 'N/A'
    

                                for pred in predicciones:
                                    mes_año = pred.get('mes_año', 'N/A')[:10]
                                    cantidad = pred.get('Prediccion_Total_Cantidad', 0)
                                    
                                    # tienda = pred.get('Tienda', 'N/A')
                                    # marca = pred.get('Marca', 'N/A')
                                    # grupo = pred.get('Grupo', 'N/A')
                                    # genero = pred.get('Genero', 'N/A')

                                    # Extraer el año y el mes por separado
                                    año = mes_año[:4]  # Extrae 'YYYY'
                                    mes = mes_año[5:7]  # Extrae 'MM'

                                    meses.append(mes_año)
                                    cantidades.append(cantidad)

                                    # Agregar la fila a la lista de filas de la tabla
                                    filas_tabla.append([año, mes, cantidad])  # Solo el año, mes y cantidad

                                                # Crear el gráfico de línea
                                    # Ajustar el tamaño del gráfico y cambiar el color de la línea
                                    fig, ax = plt.subplots(figsize=(6, 4))  # Aumentar el tamaño del gráfico

                                    # Crear el gráfico con el color personalizado para la línea
                                    ax.plot(meses, cantidades, marker='o', color='#e78ead')  # Color personalizado #e78ead
                                    ax.set_xlabel('Mes/Año')
                                    ax.set_ylabel('Predicción Total Cantidad')
                                    ax.set_title('Predicción de Ventas por Mes/Año')
                                    ax.grid(True)

                                    # Ajustar las etiquetas del eje X para que no se sobrepongan
                                    fig.autofmt_xdate()

                                # Crear el título de la tabla
                                titulo_tabla = ft.Text("PREDICCIÓN DE DEMANDA", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)
                            
                                row_titulo_form=ft.Container(
                                    
                                    content=ft.Column([
                                        titulo_tabla
                                ]), 
                                    alignment=ft.alignment.center,                                    
                                )

                                # Crear contenedores para mostrar información adicional debajo del título
                                info_tienda = ft.Text(f"TIENDA: {tienda}", size=11, color=ft.colors.BLACK)
                                info_marca = ft.Text(f"MARCA: {marca}", size=11, color=ft.colors.BLACK)
                                info_grupo = ft.Text(f"GRUPO: {grupo}", size=11, color=ft.colors.BLACK)
                                info_genero = ft.Text(f"GÉNERO: {genero}", size=11, color=ft.colors.BLACK)
                                info_talla= ft.Text(f"TALLA: {talla}", size=11, color=ft.colors.BLACK)
                                info_color = ft.Text(f"COLOR: {c_olor}", size=11, color=ft.colors.BLACK)
                                info_producto = ft.Text(f"PRODUCTO: {producto}", size=11, color=ft.colors.BLACK)

                                row_info_form=ft.Container(content=ft.Column([
                                        info_tienda,
                                        info_grupo,
                                        info_producto,
                                        info_marca,
                                        #info_genero,
                                        #info_talla,
                                        #info_color
                                ]), 
                                    alignment=ft.alignment.center_left,                                    
                                    margin=ft.margin.only(left=3)
                                )

                                # Crear la tabla de predicciones
                                tabla_predicciones = ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Año", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)),
                                        ft.DataColumn(ft.Text("Mes", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)),
                                        ft.DataColumn(ft.Text("Cantidad", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)),
                                    ],
                                    rows=[ft.DataRow(cells=[
                                        ft.DataCell(ft.Text(str(valor), color=ft.colors.BLACK, size=11)) for valor in fila
                                    ]) for fila in filas_tabla]
                                )

                                row_tabla_form=ft.Container(content=ft.Column([
                                        tabla_predicciones
                                ]), 
                                    alignment=ft.alignment.center,                                    
                                )

                                # Función para cerrar el ListView
                                def cerrar_listview(e):
                                    page.remove(objetive1_scrollable)  # Remover el contenedor del ListView
                                    page.update()  # Actualizar la página

                                # Crear un botón para cerrar el ListView
                                boton_cerrar = ft.TextButton(
                                    "Cerrar",
                                    on_click=cerrar_listview,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.RED,  # Color del texto
                                        side=ft.BorderSide(width=1, color=ft.colors.RED),  # Borde rojo                                    
                                    )
                                )

                                row_grafico_form=ft.Container(content=ft.Column([
                                        MatplotlibChart(fig, expand=True),
                                ]), 
                                    alignment=ft.alignment.center,                                    
                                )


                                # Crear un contenedor para la tabla y la información adicional
                                col_resultado = ft.Container(
                                    content=ft.Column([
                                        row_titulo_form,  # Agregar el título
                                        row_info_form,
                                        MatplotlibChart(fig, expand=True),
                                        row_tabla_form,
                                        boton_cerrar,
                                    ]),
                                    width=300,
                                    height=700,
                                    margin=ft.margin.only(left=5, right=5),
                                    padding=5,
                                    border_radius=5,
                                    border=ft.border.all(
                                        color=ft.colors.BLACK,  # Color del borde
                                        width=1  # Ancho del borde
                                    )
                                )

                                objetive1_scrollable = ft.ListView(
                                    controls=[col_resultado],
                                    expand=True, 
                                )

                                # Agregar la tabla al layout de la página
                                page.add(objetive1_scrollable)

                            else:
                                tabla_predicciones.value = "No se encontraron predicciones."

                            page.update()

                        else:
                            # Imprimir mensaje de error detallado
                            print(f"Error: {response.status_code} - {response.text}")
                            tabla_predicciones.value = f"Error: {response.status_code}"

                    except requests.exceptions.RequestException as e:
                        print(f"Ocurrió un error de red: {e}")
                        tabla_predicciones.value = f"Ocurrió un error de red: {e}"

                    except ValueError as e:
                        print(f"Error al procesar la respuesta JSON: {e}")
                        tabla_predicciones.value = f"Error al procesar la respuesta JSON: {e}"

                    except Exception as e:
                        print(f"Ocurrió un error inesperado: {e}")
                        tabla_predicciones.value = f"Ocurrió un error inesperado: {e}"

                
        #ÍCONO PARA VALIDACIONES      
        icon_valid_fumador=ft.Icon()
        icon_valid_glucosa=ft.Icon()
        icon_valid_imc=ft.Icon()

        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #ELEMENTOS DE INTERFAZ

        #variables para colores
        color="#404040"
        color_hint="#C3C7CF"
        border_radius=10

        #boton en texto -> < VOLVER
        texto_volver = ft.TextButton(
            on_click=lambda e: accion_volver_home(e, page, app_state),
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.ARROW_BACK_IOS_SHARP, color=ft.colors.WHITE, size=10),
                    ft.Container(width=5),
                    ft.Text("Volver", color=ft.colors.WHITE)
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),             
            )

        # Titulo del objetivo 1
        txt_objetivo = ft.Text("PREDICCIÓN DE LA DEMANDA", style=ft.TextStyle(size=16, weight="bold", color=ft.colors.WHITE))
        
        # Descripcion del tema
        txt_descripcion = ft.Text("Predicción de la demanda mediante machine learning", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
        imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/objetivo1.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,)
                ]),width=100)
        
        # Titulo de formulario
        txt_formulario = ft.Text("Formulario", style=ft.TextStyle(size=16, color=color))


        #------------------- Input para el GENERO-------------------
        if generos is not None:
            generos = generos
        else:
            generos = []
        
        generos = ['TODOS'] + generos 

        txt_genero=ft.Row(
            [
                ft.Icon(name=ft.icons.TRANSGENDER, color=color_hint),
                ft.Text("Genero", color=color)            
            ]
        )        
        ip_genero = ft.Dropdown(
            label="Seleccione...", 
            options=[ft.dropdown.Option(genero) for genero in generos], 
            width=300, 
            on_change=lambda e: seleccionado(e, col_genero),
            color="#6dbadc",
            value="TODOS"            
        )

        # txt_error_genero = ft.Text("", color="red", size=12)

         #------------------- Input para el TALLA-------------------
        if tallas is not None:
            tallas = tallas
        else:
            tallas = []
        
        tallas = ['TODOS'] + tallas 

        txt_tallas=ft.Row(
            [
                ft.Icon(name=ft.icons.RULE, color=color_hint),
                ft.Text("Talla", color=color)            
            ]
        )        
        ip_talla = ft.Dropdown(
            label="Seleccione...", 
            options=[ft.dropdown.Option(talla) for talla in tallas], 
            width=300, 
            on_change=lambda e: seleccionado(e, col_talla),
            color="#6dbadc",   
            value="TODOS"          
        )


        # ------------------- Input para el Color-------------------
        if colores is not None:
            colores = colores
        else:
            colores = []

        colores = ['TODOS'] + colores 
        txt_Color=ft.Row(
            [
                ft.Icon(name=ft.icons.PALETTE, color=color_hint),
                ft.Text("Color", color=color)            
            ]
        )        
        ip_color = ft.Dropdown(
            label="Seleccione...", 
            options=[ft.dropdown.Option(color) for color in colores], 
            width=300,  # Ajusta el ancho según tu preferencia
            on_change=lambda e: seleccionado(e, col_color),
            color="#6dbadc", 
            value="TODOS"            
        )

        # -----------------Input para el DESCRIPCION----------------------
        if productos is not None:
            productos = productos
        else:
            productos = []
        productos = ['TODOS'] + productos 
        # Lista de opciones
        txt_producto=ft.Row(
            [
                ft.Icon(name=ft.icons.DEVICES, color=color_hint),
                ft.Text("Producto", color=color)            
            ]
        )
    
        # Campo de búsqueda
        # txt_busqueda_producto = ft.TextField(
        #     hint_text="Buscar producto...",
        #     hint_style=ft.TextStyle(color=color_hint),  # Color del texto de sugerencia
        #     text_style=ft.TextStyle(color=color),  # Color del texto que escribe el usuario
        #     prefix_icon=ft.icons.SEARCH,  # Ícono de búsqueda antes del texto
        #     on_change=lambda e: actualizar_dropdown_producto(e.control.value, ip_producto, productos)
        # )
        
        # Dropdown con opciones
        
        ip_producto = ft.Dropdown(
            label="Seleccione...", 
            options=[ft.dropdown.Option(producto) for producto in productos], 
            width=300,  
            color="#6dbadc",
            on_change=lambda e: seleccionado(e, col_producto),
            value="TODOS" 
        )
        
        # def actualizar_dropdown_producto(busqueda, dropdown, productos):
        #     dropdown.options = [ft.dropdown.Option(producto) for producto in productos if busqueda.lower() in producto.lower()]
        #     dropdown.update() 
        
        # -----------------Input para el GRUPO----------------------
        # Lista de opciones
        print(opciones)

        txt_grupo=ft.Row(
            [
                ft.Icon(name=ft.icons.CATEGORY, color=color_hint),
                ft.Text("Grupo", color=color)            
            ]
        )
    
        # Campo de búsqueda
        txt_busqueda = ft.TextField(
            hint_text="Buscar grupo...",
            hint_style=ft.TextStyle(color=color_hint),  # Color del texto de sugerencia
            text_style=ft.TextStyle(color=color),  # Color del texto que escribe el usuario
            prefix_icon=ft.icons.SEARCH,  # Ícono de búsqueda antes del texto
            on_change=lambda e: actualizar_dropdown(e.control.value, ip_grupos, opciones)
        )
        
        # Dropdown con opciones
        
        ip_grupos = ft.Dropdown(
            label="Seleccione...", 
            options=[ft.dropdown.Option(opcion) for opcion in opciones], 
            width=300,  
            color="#6dbadc",
            on_change=lambda e: actualizar_combos(e.control.value, ip_marca, ip_genero, ip_talla, ip_color, ip_producto, token) 
        )
        
        def actualizar_dropdown(busqueda, dropdown, opciones):
            dropdown.options = [ft.dropdown.Option(opcion) for opcion in opciones if busqueda.lower() in opcion.lower()]
            dropdown.update() 

        #----------------------- Input para el MESES ------------------------
        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Formato: día/mes/año

        # Crear el Row con la fecha actual
        txt_meses = ft.Row(
            [
                ft.Icon(name=ft.icons.CALENDAR_MONTH, color=color_hint),
                ft.Text(f"Fecha actual: {fecha_actual}", color=color)  # Mostrar la fecha actual
            ]
        )
        
        
        #----------------------- Input para el tienda -----------------------
        txt_tienda=ft.Row(
            [ 
                ft.Icon(name=ft.icons.STORE, color=color_hint),
                ft.Text("Tiendas", color=color)            
            ]
        ) 
        ip_tienda = ft.Dropdown(
            label="Seleccione...", 
            options=[
                ft.dropdown.Option("TODOS", "TODOS"),
                ft.dropdown.Option("ALMACÉN GENERAL", "ALMACÉN GENERAL"),
                ft.dropdown.Option("TIENDA MANUEL RUIZ CH", "TIENDA MANUEL RUIZ CH"),
                ft.dropdown.Option("TIENDA GAMARRA", "TIENDA GAMARRA"),
                ft.dropdown.Option("TIENDA MEGA PLAZA CH", "TIENDA MEGA PLAZA CH"),
                ft.dropdown.Option("TIENDA BOULEVARD", "TIENDA BOULEVARD"),
                ft.dropdown.Option("TIENDA GRAU", "TIENDA GRAU"),
                ft.dropdown.Option("TIENDA ESPINAR CH", "TIENDA ESPINAR CH"),
                ft.dropdown.Option("TIENDA AYACUCHO", "TIENDA AYACUCHO"),
                ft.dropdown.Option("TIENDA RPCAJAMARCA", "TIENDA RPCAJAMARCA"),
            ],
            width=300,  # Ajusta el ancho según tu preferencia
            on_change=lambda e: seleccionado(e, col_tienda),
            color="#6dbadc",  
            value="TODOS" 
        )

        #----------------------- Input para el marca -------------------------
        # Lista de opciones
        if opciones_marca is not None:
            opciones_marca = opciones_marca
        else:
            opciones_marca = []
        
        opciones_marca = ['TODOS'] + opciones_marca

        txt_marca=ft.Row(
            [ 
                ft.Icon(name=ft.icons.CODE, color=color_hint),
                ft.Text("Marcas", color=color)            
            ]
        ) 
        
        # Campo de búsqueda
        # txt_busqueda_marca = ft.TextField(
        #     hint_text="Buscar marca...",
        #     hint_style=ft.TextStyle(color=color_hint),  # Color del texto de sugerencia
        #     text_style=ft.TextStyle(color=color),  # Color del texto que escribe el usuario
        #     prefix_icon=ft.icons.SEARCH,  # Ícono de búsqueda antes del texto
        #     on_change=lambda e: actualizar_dropdown_marca(e.control.value, ip_marca, opciones_marca)
        # )

        ip_marca = ft.Dropdown(
            label="Seleccione...", 
            options=[ft.dropdown.Option(opcion) for opcion in opciones_marca],  # Inicializa el dropdown
            width=300,  # Ajusta el ancho
            color="#6dbadc",    # Establece el color del texto
            on_change=lambda e: seleccionado(e, col_marca),
            value="TODOS" 
        )

        # def actualizar_dropdown_marca(busqueda, dropdown, opciones):
        #     dropdown.options = [ft.dropdown.Option(opcion) for opcion in opciones if busqueda.lower() in opcion.lower()]
        #     dropdown.update() 

        # ------------------ botón -> Diagnosticar ---------------------------
        btn_diagnosticar= ft.FilledButton(
            text="PREDECIR",
            width=300, 
            height=40,  
            on_click=lambda e:  diagnosticar(e),
            style=ft.ButtonStyle(
                shape=ft.StadiumBorder(),
                color={
                    ft.ControlState.HOVERED: ft.colors.WHITE,
                    ft.ControlState.FOCUSED: ft.colors.WHITE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                },
                bgcolor={
                ft.ControlState.HOVERED: color_hovered,
                ft.ControlState.DEFAULT: color_primary,
            },
            )
            )

        #----------------------------------------------------------------------------------------------------------------------------------------------

        #CONTAINERS PARA SEPARAR COLUMNAS DE ELEMENTOS
        col_volver=ft.Container(content=ft.Row([
                texto_volver
            ], alignment=ft.MainAxisAlignment.END
            ), width=360, 
            margin=ft.margin.only(bottom=5, right=5), 
            )
        
        col_derecha=ft.Container(content=ft.Column([
                    txt_objetivo,
                    txt_descripcion

            ]), width=200)
        col_izquierda=ft.Container(content=ft.Column([
                    imagen_principal
            ]), width=100)
        
        col_titulo_form=ft.Container(content=ft.Column([
                txt_formulario
            ]
            ), width=300, 
            margin=5,
            alignment=ft.alignment.center,             
            )

        col_genero=ft.Container(content=ft.Column([
                txt_genero,
                ip_genero
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_talla=ft.Container(content=ft.Column([
                txt_tallas,
                ip_talla
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_color=ft.Container(content=ft.Column([
                txt_Color,
                ip_color
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_valid_genero=ft.Container(content=ft.Row([
                icon_valid_fumador,
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        
        col_grupos=ft.Container(content=ft.Column([
                txt_grupo,
                txt_busqueda,
                ip_grupos
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_producto=ft.Container(content=ft.Column([
                txt_producto,
                # txt_busqueda_producto,
                ip_producto
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_valid_grupos=ft.Container(content=ft.Row([
                icon_valid_fumador,
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        
        col_meses=ft.Container(content=ft.Column([
                txt_meses                
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )

        col_tienda=ft.Container(content=ft.Column([
                txt_tienda,
                ip_tienda
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_valid_tienda=ft.Container(content=ft.Row([
                icon_valid_fumador,
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )

        col_marca=ft.Container(content=ft.Column([
                txt_marca,
                # txt_busqueda_marca,
                ip_marca
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_valid_marca=ft.Container(content=ft.Row([
                icon_valid_fumador,
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )

        col_boton=ft.Container(content=ft.Column([
                btn_diagnosticar
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )

        #----------------------------------------------------------------------------------------------------------------------------------------------  
        #CONTAINERS PARA SEPARAR FILAS DE ELEMENTOS
        row_volver_container=ft.Container(content=ft.Column([
                col_volver
        ]
        ), 
        border=None,
        )
        row_titulo_container=ft.Container(content=ft.Row([
                col_derecha,
                col_izquierda
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER
        ), 
        border=None,
        )

        row_titulo_form=ft.Container(content=ft.Column([
                col_titulo_form
        ]
        ), 
        #width=360,
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_genero=ft.Container(content=ft.Column([
                col_genero,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_color=ft.Container(content=ft.Column([
                col_color,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_talla=ft.Container(content=ft.Column([
                col_talla,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_grupo=ft.Container(content=ft.Column([
                col_grupos,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_producto=ft.Container(content=ft.Column([
                col_producto,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_meses=ft.Container(content=ft.Column([
                col_meses,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border
        )


        row_tienda=ft.Container(content=ft.Column([
                col_tienda,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border
        )

        row_marca=ft.Container(content=ft.Column([
                col_marca,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border
        )

        row_boton=ft.Container(content=ft.Column([
                col_boton
        ]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all() 
        #width=360,
        )

        #----------------------------------------------------------------------------------------------------------------------------------------------       
        #CONTAINER PRINCIPAL

        row_superior=ft.Container(content=ft.Column([
                row_volver_container,
                row_titulo_container,              
        ],spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ), 
        bgcolor=color_primary,
        padding=ft.padding.only(left=20, top=10, bottom=20, right=20),
        )

        row_form=ft.Container(content=ft.Column([
                row_titulo_form,
                row_meses,
                row_grupo,
                row_tienda,
                row_marca,
                row_genero,
                row_talla,
                row_color,
                row_producto,
                row_boton,
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
                ),
                bgcolor=ft.colors.WHITE,
                margin=10,
                padding=10,
                width=350,
                alignment=ft.alignment.center,
                border_radius=20
                )

        principal_container=ft.Container(content=ft.Column([
                row_superior,
                row_form
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
        ), 
        width=360,
        alignment=ft.alignment.center,
        #border=ft.border.all(),
        )


        objetive1_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True, 
        )

        #page.controls.clear()
        page.controls.append(objetive1_scrollable)
        page.update()



