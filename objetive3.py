import flet as ft
import requests
from login import login_view
from datetime import datetime
from validation import validate_radiobutton, validate_intervalo
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_check, color_error
from menubar import menubar
from urlsapi import HTTP_OBJ_3

#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 3
def objetive3_view(page, app_state):
        if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return
        #Obtener token
        token =app_state.token

        global prediccion_resultado        
        API_URL = HTTP_OBJ_3

        page.padding=0
        #----------------------------------------------------------------------------------------------------------------------------------------------
        #MÉTODOS  

        #filtro para validaciones
        def filtro_valid_objetive3(page, data_values, data_keys, errores):
            # Validaciones
            for i in range(len(data_values)):
                value = data_values[i]
                key = data_keys[i]
                

                if key == "etnia":
                    error = validate_radiobutton(page, value, col_valid_etnia, txt_valid_etnia, col_etnia, icon_valid_etnia)
                elif key == "horasDormidas":
                    error = validate_intervalo(page, value, col_valid_horas, txt_valid_horas, ip_horas, icon_valid_horas, 0, 24)
                elif key == "fumador":
                    error = validate_radiobutton(page, value, col_valid_fumador, txt_valid_fumador, col_fumador, icon_valid_fumador)
                elif key == "bebedorFrecuente":
                    error = validate_radiobutton(page, value, col_valid_bebedor, txt_valid_bebedor, col_bebedor, icon_valid_bebedor)
                elif key == "actividadFisica":
                    error = validate_radiobutton(page, value, col_valid_fisica, txt_valid_fisica, col_fisica, icon_valid_fisica)
                else:
                    error = None

                if error:
                    errores.append(f"Error en {key}: {error}")

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
                "Nombre del paciente": ip_paciente.value,
                "edadRango": ip_edad.value,
                "genero": genero_option,
                "etnia": ip_etnia.value,
                "fumador": ip_fumador.value,
                "bebedorFrecuente": ip_bebedor.value,
                "actividadFisica": ip_fisica.value,
                "horasDormidas": ip_horas.value,
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

            #Llamada al método para validaciones
            filtro_valid_objetive3(page, datos_values, datos_keys, errores)

            # Imprimir errores

            list_errores="\n".join(errores)


            if errores:
                error_alert_objetive1 = ft.AlertDialog(
                    title=ft.Text("Error", color=ft.colors.RED),
                    content=ft.Text(list_errores, color=ft.colors.RED),
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(10)
                )
                page.open(error_alert_objetive1)
            
                # Imprimir los datos en la consola
                print(datos)

            else:

                # headers = {
                #         'Authorization': f'Token {token}',
                #         'Content-Type': 'application/json'}
                # Enviar una solicitud POST a la API

                # Enviar una solicitud POST a la API
                try:
                    headers = {
                        'Authorization': f'Token {token}',
                        'Content-Type': 'application/json'}
                    response = requests.post(API_URL, json=datos, headers=headers)

                    if response.status_code == 201:
                        aprobado=ft.Container(content=ft.Row([
                            ft.Icon(name=ft.icons.CHECK_CIRCLE_ROUNDED,color=color_check, size=30),
                            ft.Text("Predicción Realizada", color=color, size=14)
                        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER))
                        alert_aprobado = ft.AlertDialog(
                            content=aprobado,
                            bgcolor=ft.colors.WHITE,
                            shape=ft.RoundedRectangleBorder(10), 
                        )
                        page.open(alert_aprobado)
                        time.sleep(1.5)
                        page.close(alert_aprobado)
                        # Manejar la respuesta exitosa
                        response_json = response.json()
                        prediction_value = response_json.get('prediccion', [0])[0]
                        print(prediction_value)

                        if prediction_value == 0:
                            mensaje = "Predicción: Pertenece al grupo de precaución mayor"
                        elif prediction_value == 1:
                            mensaje = "Predicción: Pertenece al grupo de precaución menor"
                        else:
                            mensaje = "Predicción: Pertenece al grupo de precaución intermedia"
                        
                        prediccion_resultado.value = mensaje
                        print(mensaje)                        
                        page.update()

                    else:
                        # Imprimir mensaje de error detallado
                        print(f"Error: {response.status_code} - {response.text}")
                        prediccion_resultado.value = f"Error: {response.status_code}"
                except Exception as e:
                    print(f"Ocurrió un error: {e}")
                    prediccion_resultado.value = f"Ocurrió un error: {e}"

        #----------------------------------------------------------------------------------------------------------------------------------------------
         
        #OBTENER DATOS DEL PACIENTE

        #Nombre completo
        nombres = app_state.paciente_data.get('nombres', 'Nombres')
        apPaterno = app_state.paciente_data.get('apPaterno', 'Apellido Paterno')
        apMaterno = app_state.paciente_data.get('apMaterno', 'Apellido Materno')
        nombre_completo = f"{nombres} {apPaterno} {apMaterno}"
        #Género
        genero = app_state.paciente_data.get('genero', 'Género')
        #Transformando valor de género
        if genero == "Femenino":
            genero_option=0
        else:
            genero_option=1
        #Edad
        fecha_nacimiento = app_state.paciente_data.get('fecha_nacimiento', 'Fecha Nacimiento')
        fecha_nacimiento_str = datetime.strptime(fecha_nacimiento, '%Y-%m-%d') #cambiar de string a date
        hoy = datetime.today() #obtener fecha actual
        edad = hoy.year - fecha_nacimiento_str.year
        #Verificar si la persona no ha cumplido años este año
        if (hoy.month, hoy.day) < (fecha_nacimiento_str.month, fecha_nacimiento_str.day):
            edad -= 1
        

        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #ÍCONO PARA VALIDACIONES
 
        icon_valid_paciente=ft.Icon()            
        icon_valid_edad=ft.Icon()
        icon_valid_genero=ft.Icon()
        icon_valid_etnia=ft.Icon()
        icon_valid_fumador=ft.Icon()
        icon_valid_bebedor=ft.Icon()
        icon_valid_fisica=ft.Icon()
        icon_valid_horas=ft.Icon() 

        #----------------------------------------------------------------------------------------------------------------------------------------------

        #ELEMENTOS DE INTERFAZ

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

        #titulo del objetivo 3
        txt_objetivo = ft.Text("Segmentación de pacientes", style=ft.TextStyle(size=20, weight="bold", color=ft.colors.WHITE))
        
        #breve descripcion del tema
        txt_descripcion = ft.Text("Clasificación de nivel de riesgo bajo estilo de vida", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
        imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj3.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,)
                ]),width=100)
        
        #titulo de formulario
        txt_formulario = ft.Text("Formulario para Segmentación", style=ft.TextStyle(size=16, color='#333333'))

        #input para el nombre del paciente
        ip_paciente=ft.TextField(
            label="Nombre del paciente",
            prefix_icon=ft.icons.PERSON,
            hint_text="Nombre del paciente",
            autofocus=True,
            content_padding=0,
            color=color_hint,
            text_size=14,
            hint_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                weight="normal"
                ),
            label_style=ft.TextStyle(
                color=color,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            disabled=True,
            border_color="#cccccc",
            read_only=True,
            value=nombre_completo,
            border_radius=border_radius,
        )

        #input para la edad
        ip_edad=ft.TextField(
            label="Edad",
            keyboard_type="number",
            prefix_icon=ft.icons.CALENDAR_MONTH,
            hint_text="0",
            content_padding=0,
            color=color_hint,
            text_size=14,
            hint_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color=color,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            selection_color="#333333",
            prefix_style=ft.TextStyle(
                bgcolor=ft.colors.BLACK,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            disabled=True,
            border_color="#cccccc",
            read_only=True,
            value=str(edad),
            border_radius=border_radius,
        )

        #input para la genero
        ip_genero=ft.TextField(
            label="Género",
            keyboard_type="number",
            prefix_icon=ft.icons.MALE,
            hint_text="0",
            content_padding=0,
            color=color_hint,
            text_size=14,
            hint_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color=color,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            selection_color="#333333",
            prefix_style=ft.TextStyle(
                bgcolor=ft.colors.BLACK,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            disabled=True,
            border_color="#cccccc",
            read_only=True,
            value=genero,
            border_radius=border_radius,
        )

        #input para el Estado de Fumador
        txt_fumador=ft.Row(
            [
                ft.Icon(name=ft.icons.SMOKING_ROOMS, color=color_hint),
                ft.Text("Fumador", color=color)
            ]
        )        
        ip_fumador = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Si",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )), 
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_fumador),
            )
        
        #texto para validacion de campo ip_fumador
        txt_valid_fumador=ft.Text()
        
        #input para bebedor frecuente
               
        txt_bebedor=ft.Row(
            [
                ft.Icon(name=ft.icons.LIQUOR, color=color_hint),
                ft.Text("¿Bebedor frecuente?", color=color)
            ]
        )        
        ip_bebedor = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Si",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )), 
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_bebedor),
            )
        
        #texto para validacion de campo ip_fumador
        txt_valid_bebedor=ft.Text()
         
        
        txt_fisica=ft.Row(
            [
                ft.Icon(name=ft.icons.DIRECTIONS_RUN, color=color_hint),
                ft.Text("¿Actividad física frecuente?", color=color)
            ]
        )        
        ip_fisica = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Si",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )), 
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_fisica),
            )
        
        #texto para validacion de campo ip_fumador
        txt_valid_fisica=ft.Text()

        #input para horas dormidas
        ip_horas=ft.TextField(
            label="Horas dormidas",
            keyboard_type="number",
            prefix_icon=ft.icons.HOTEL,
            hint_text="0",
            content_padding=0,
            color=color,
            text_size=14,
            hint_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color=color,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            focused_border_color=ft.colors.BLUE_300,
            focused_border_width=1,
            border_color="#dddddd",
            border_radius=border_radius,
        )
        
        txt_valid_horas=ft.Text()

        #input para la etnia
        txt_etnia=ft.Row(
            [
                ft.Icon(name=ft.icons.DIVERSITY_3, color=color_hint),
                ft.Text("Etnia", color=color)
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ])

        ip_etnia = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="Indígena",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Asiático",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="2", 
                label="Negro",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="3", 
                label="Hispano",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="5", 
                label="Blanco",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="4", 
                label="Otro",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_etnia),
            )
        #texto para validacion de campo ip_etnia
        txt_valid_etnia=ft.Text()

        #botón -> Diagnosticar
        btn_diagnosticar= ft.FilledButton(
            text="Segmentar",
            width=300, 
            height=40,  
            on_click=diagnosticar,
            #on_click=ir_home,  #AQUI LLAMAMOS A LA FUNCIÓN QUE NOS PERMITIRÁ OBTENER LA PREDICCIÓN
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

        #etiqueta -> Obtener resultado
        txt_sub_resultado= ft.Text("Resultado Obtenido por factores de calidad de vida:", style=ft.TextStyle(size=16, color=color))

        #text, para mostrar el resultado de predicción
        prediccion_resultado=ft.Text("Resultado...", style=ft.TextStyle(size=15, color=color_primary))

        #----------------------------------------------------------------------------------------------------------------------------------------------

        #CONTAINERS PARA SEPARAR COLUMNAS DE ELEMENTOS
        col_volver=ft.Container(content=ft.Row([
                texto_volver
            ], alignment=ft.MainAxisAlignment.END
            ), width=360, 
            margin=5, 
            #border=ft.border.all()
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
            margin=20,
            alignment=ft.alignment.center, 
            #border=ft.border.all()
            )

        col_paciente=ft.Container(content=ft.Column([
                ip_paciente
            ]
            ), width=300,
            #border=ft.border.all()
            )
        col_edad=ft.Container(content=ft.Column([
                ip_edad
            ]
            ), width=300, 
            #border=ft.border.all()
            )

        col_genero=ft.Container(content=ft.Column([
                ip_genero
            ]
            ), width=300, 
            #border=ft.border.all()
            )     
        
        col_fumador=ft.Container(content=ft.Column([
                txt_fumador,
                ip_fumador
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=border_radius  
            #border=ft.border.all()
            )
        col_valid_fumador=ft.Container(content=ft.Row([
                icon_valid_fumador,
                txt_valid_fumador    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        
        col_bebedor=ft.Container(content=ft.Column([
                txt_bebedor,
                ip_bebedor
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=border_radius  
            #border=ft.border.all()
            )
        col_valid_bebedor=ft.Container(content=ft.Row([
                icon_valid_bebedor,
                txt_valid_bebedor
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,
            #border=ft.border.all()
            )
        
        col_fisica=ft.Container(content=ft.Column([
                txt_fisica,
                ip_fisica
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=border_radius  
            #border=ft.border.all()
            )
        col_valid_fisica=ft.Container(content=ft.Row([
                icon_valid_fisica,
                txt_valid_fisica
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,
        )

        col_horas=ft.Container(content=ft.Column([
                ip_horas
            ]
            ), width=300,
            #border=ft.border.all()
            )  
        col_valid_horas=ft.Container(content=ft.Row([
                icon_valid_horas,
                txt_valid_horas
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,
        )
        
        col_etnia=ft.Container(content=ft.Column([
                txt_etnia,
                ip_etnia
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=border_radius  
            #border=ft.border.all()
            )
        col_valid_etnia=ft.Container(content=ft.Row([
                icon_valid_etnia,
                txt_valid_etnia    
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
        
        col_t_resultado=ft.Container(content=ft.Column([
                txt_sub_resultado,
            ]
            ), width=300,
            height=40, 
            margin=ft.margin.only(left=10,top=10,right=10),
            )
        col_resultado=ft.Container(content=ft.Column([
                prediccion_resultado
            ]
            ), width=300,
            height=150, 
            margin=10,
            padding=20, 
            border_radius=10,
            border=ft.border.all(
                color=ft.colors.BLUE_200,  # Color del borde
                width=1  # Ancho del borde)
                )
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
        row_paciente=ft.Container(content=ft.Column([
                col_paciente
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),
        margin=ft.margin.only(top=10),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )
        row_genero=ft.Container(content=ft.Column([       
                col_genero
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),
        margin=ft.margin.only(top=10, bottom=10), 
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_edad=ft.Container(content=ft.Column([         
                col_edad
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),
        margin=ft.margin.only(top=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_fumador=ft.Container(content=ft.Column([
              col_fumador,
              col_valid_fumador
        ], spacing = 0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center, 
        )

        row_bebedor=ft.Container(content=ft.Column([
              col_bebedor,
              col_valid_bebedor
        ], spacing = 0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center, 
        )

        row_fisica=ft.Container(content=ft.Column([
              col_fisica,
              col_valid_fisica
        ], spacing = 0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center,
        #border=ft.border.all() 
        )

        row_horas=ft.Container(content=ft.Column([
              col_horas,
              col_valid_horas
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        )

        row_etnia=ft.Container(content=ft.Column([
              col_etnia,
              col_valid_etnia
        ], spacing = 0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center, 
        )
        row_boton=ft.Container(content=ft.Column([
              col_boton
        ]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all() 
        #width=360,
        )
        row_resultado=ft.Container(content=ft.Column([
                col_t_resultado,
                col_resultado,
        ]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all() ,
        width=300,
        )


        
        #----------------------------------------------------------------------------------------------------------------------------------------------       
        #CONTAINER PRINCIPAL

        row_superior=ft.Container(content=ft.Column([
              row_volver_container,
              row_titulo_container,
              
        ],spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ), bgcolor=color_primary, 
        padding=ft.padding.only(left=20, top=10, bottom=20, right=20),
        )

        row_form=ft.Container(content=ft.Column([
              row_titulo_form,
              row_paciente,
              row_edad,
              row_genero,
              row_etnia,
              row_horas,
              row_fisica,
              row_fumador,
              row_bebedor,
              row_boton,
              row_resultado
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
        )

        objetive3_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
    )

        #page.controls.clear()
        page.controls.append(objetive3_scrollable)
        page.update()