import flet as ft
import requests
# from message_whatsapp import message_whatsapp
from login import login_view
from api_whatsapp import message_whatsapp
from datetime import datetime
from validation import validate_radiobutton, validate_intervalo
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_check, color_error
from menubar import menubar
from urlsapi import HTTP_OBJ_1

#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 1
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

        global prediccion_resultado  
        API_URL = HTTP_OBJ_1
        
        #----------------------------------------------------------------------------------------------------------------------------------------------
        #MÉTODOS  

        #filtro para validaciones
        def filtro_valid_objetive1(page, data_values, data_keys, errores):
            # Validaciones
            for i in range(len(data_values)):
                value = data_values[i]
                key = data_keys[i]
                      
                if key == "Hipertension":
                    error = validate_radiobutton(page, value, col_valid_hipertension, txt_valid_hipertension, col_hipertension, icon_valid_hipertension)
                elif key == "Cardiopatia":
                    error = validate_radiobutton(page, value, col_valid_cardiopatia, txt_valid_cardiopatia, col_cardiopatia, icon_valid_cardiopatia)
                elif key == "TipoTrabajo":
                    error = validate_radiobutton(page, value, col_valid_trabajo, txt_valid_trabajo, col_trabajo, icon_valid_trabajo)
                elif key == "Nivel_GlucosaPromedio":
                    error = validate_intervalo(page, value, col_valid_glucosa, txt_valid_glucosa, ip_glucosa, icon_valid_glucosa, 30, 300)
                elif key == "ICM":
                    error = validate_intervalo(page, value, col_valid_imc, txt_valid_imc, ip_imc, icon_valid_imc, 10, 100)
                elif key == "EstadoFumador":
                    error = validate_radiobutton(page, value, col_valid_fumador, txt_valid_fumador, col_fumador, icon_valid_fumador)
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
                "Genero": genero_option,  
                "Edad": ip_edad.value,  
                "Hipertension": ip_hipertension.value, 
                "Cardiopatia": ip_cardiopatia.value, 
                "TipoTrabajo": ip_trabajo.value,  
                "Nivel_GlucosaPromedio": ip_glucosa.value,  
                "ICM": ip_imc.value,  
                "EstadoFumador": ip_fumador.value,  
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
            filtro_valid_objetive1(page, datos_values, datos_keys, errores)

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
                # Imprimir los datos en la consola
                print(datos)

            else: 

                headers = {
                        'Authorization': f'Token {token}',
                        'Content-Type': 'application/json'}
                # Enviar una solicitud POST a la API
                try:
    
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
                        response_json = response.json()
                        
                        prediction_value = response_json.get('prediccion', [0])
                        print(prediction_value)

                        if prediction_value == 0:
                            mensaje1 = "Nos complace informarle que"
                            mensaje2 = "presenta BAJA probabilidad de riesgo de un accidente cerebrovascular (ACV) en su evaluación actual."
                            
                        else:
                            mensaje1 = "Le informamos que"
                            mensaje2 = "presenta ALTA probabilidad de riesgo de un accidente cerebrovascular (ACV) en su evaluación actual."
                            

                        prediccion = f"Estimado/a {ip_paciente.value},\n\n{mensaje1}, tras revisar los resultados de sus pruebas, {mensaje2}"
                        prediccion_resultado.value = prediccion

                        # número de prueba para enviar el mensaje, incluir el 51 por código del país
                        telefono = f"51{ip_telefono.value}"

                       
                        print(ip_genero.value)
                        w_hipertension = "No" if int(ip_hipertension.value) == 0 else "Sí"
                        w_cardiopatia = "No" if int(ip_cardiopatia.value) == 0 else "Sí"
                        
                        if int(ip_trabajo.value) == 0:
                            w_trabajo = "Trabajador para el gobierno"
                        elif int(ip_trabajo.value) == 1:
                            w_trabajo = "Nunca trabajó"
                        elif int(ip_trabajo.value) == 2:
                            w_trabajo = "Trabajador privado"
                        else:
                            w_trabajo = "Trabajador por cuenta propia"

                        if int(ip_fumador.value) == 0:
                            w_fumador = "No opina"
                        elif int(ip_fumador.value) == 1:
                            w_fumador = "Anteriormente fumó"
                        elif int(ip_fumador.value) == 2:
                            w_fumador = "Nunca fumó"
                        else:
                            w_fumador = "Fuma"

                        # Llamar a la función para enviar el mensaje de WhatsApp
                        message_whatsapp(page, ip_paciente.value, mensaje1, mensaje2, telefono, genero, ip_edad.value, w_hipertension, w_cardiopatia, w_trabajo, w_fumador, ip_glucosa.value, ip_imc.value)
                        print(prediccion)
                        page.update()

                    else:
                        # Imprimir mensaje de error detallado
                        print(f"Error: {response.status_code} - {response.text}")
                        prediccion_resultado.value = f"Error: {response.status_code}"

                except requests.exceptions.RequestException as e:
                    print(f"Ocurrió un error de red: {e}")
                    prediccion_resultado.value = f"Ocurrió un error de red: {e}"

                except ValueError as e:
                    print(f"Error al procesar la respuesta JSON: {e}")
                    prediccion_resultado.value = f"Error al procesar la respuesta JSON: {e}"

                except Exception as e:
                    print(f"Ocurrió un error inesperado: {e}")
                    prediccion_resultado.value = f"Ocurrió un error inesperado: {e}"

        

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
        celular = app_state.paciente_data.get('celular', 'Celular')
        
         #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #ÍCONO PARA VALIDACIONES
       
        icon_valid_trabajo=ft.Icon()
        icon_valid_hipertension=ft.Icon()
        icon_valid_cardiopatia=ft.Icon()
        icon_valid_fumador=ft.Icon()
        icon_valid_glucosa=ft.Icon()
        icon_valid_imc=ft.Icon()

        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #ELEMENTOS DE INTERFAZ

        #variables para colores
        color="#404040"
        color_hint="#C3C7CF"
        border_radius=10

        #input pde prueba para ingresar el número de celular que recibirá el mensaje del resultado
        ip_telefono=ft.TextField(
            label="Teléfono",
            prefix_icon=ft.icons.PERSON,
            hint_text="000 000 000",
            autofocus=True,
            content_padding=0,
            color="#333333",
            text_size=14,
            hint_style=ft.TextStyle(
                color="#cccccc",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                weight="normal"
                ),
            label_style=ft.TextStyle(
                color="#cccccc",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            selection_color="#333333",
            cursor_color="#333333",
            fill_color=ft.colors.WHITE,
            focused_border_color=ft.colors.BLUE_300,
            focused_border_width=1,
            border_color="#cccccc",
            value=celular,
            border_radius=border_radius,
        )



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

        #titulo del objetivo 1
        txt_objetivo = ft.Text("Diagnóstico de ACV", style=ft.TextStyle(size=20, weight="bold", color=ft.colors.WHITE))
        
        #breve descripcion del tema
        txt_descripcion = ft.Text("Diagnóstico rápido realizado mediante machine learning", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
        imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj1.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,)
                ]),width=100)
        
        #titulo de formulario
        txt_formulario = ft.Text("Formulario para diagnóstico", style=ft.TextStyle(size=16, color=color))

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
            fill_color=ft.colors.WHITE,
            disabled=True,
            border_color="#cccccc",
            read_only=True,
            value=genero,
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

        #input para el tipo de trabajo
        txt_trabajo=ft.Row(
            [
                ft.Icon(name=ft.icons.WORK_OUTLINE, color=color_hint),
                ft.Text("Tipo de Trabajo", color=color)
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ]
        )        
        ip_trabajo = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="Trabajador para el gobierno",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Nunca trabajó",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="2", 
                label="Trabajador privado",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="3", 
                label="Trabajador por cuenta propia",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_trabajo),
            )
        
        #texto para validacion de campo ip_trabajo
        txt_valid_trabajo=ft.Text()

        #input para la hipertencion
        txt_hipertension=ft.Row(
            [
                ft.Icon(name=ft.icons.MEDICAL_SERVICES_OUTLINED, color=color_hint),
                ft.Text("Hipertension", color=color)
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ]
        )        
        ip_hipertension = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Sí",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_hipertension),)
        
        #texto para validacion de campo ip_hipertension
        txt_valid_hipertension=ft.Text()

        #input para la cardiopatia
        txt_cardiopatia= ft.Row(
            [
                ft.Icon(name=ft.icons.MEDICAL_SERVICES_OUTLINED, color=color_hint),
                ft.Text("Cardiopatia", color=color)
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ])

        ip_cardiopatia = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Sí",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_cardiopatia),)
        
        #texto para validacion de campo ip_cardiopatia
        txt_valid_cardiopatia=ft.Text()

        #input para el Estado de Fumador
        txt_fumador=ft.Row(
            [
                ft.Icon(name=ft.icons.SMOKING_ROOMS, color=color_hint),
                ft.Text("Estado de Fumador", color=color)
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ]
        )        
        ip_fumador = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No opina",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Anteriormente fumó",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="2", 
                label="Nunca fumó",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ft.Radio(
                value="3", 
                label="Fuma",
                label_style=ft.TextStyle(
                color=color,
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=lambda e: seleccionado(e, col_fumador),)

        #input para el nivel de glucosa promedio
        ip_glucosa=ft.TextField(
            label="Nivel de Glucosa Promedio",
            keyboard_type="number",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
            hint_text="0",
            content_padding=0,
            color=color,
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
            border_color="#cccccc",
            border_radius=border_radius,
            )
        
        #texto para validacion de campo ip_glucosa
        txt_valid_glucosa=ft.Text()

        #input para el IMC
        ip_imc= ft.TextField(
            label="IMC",
            keyboard_type="number",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
            hint_text="0",
            content_padding=0,
            color=color,
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
            border_color="#cccccc",
            border_radius=border_radius,)
        
        #texto para validacion de campo ip_imc
        txt_valid_imc=ft.Text()
        
        #texto para validacion de campo ip_fumador
        txt_valid_fumador=ft.Text()

        #botón -> Diagnosticar
        btn_diagnosticar= ft.FilledButton(
            text="Diagnosticar",
            width=300, 
            height=40,  
            on_click=lambda e: diagnosticar(e),
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
        txt_sub_resultado= ft.Text("Resultado Obtenido:", style=ft.TextStyle(size=16, color="#333333"))

        #text, para mostrar el resultado de predicción
        prediccion_resultado=ft.Text("Resultado...", style=ft.TextStyle(size=15, color=color_primary))

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
            margin=20,
            alignment=ft.alignment.center, 
            #border=ft.border.all()
            )
        
        col_paciente=ft.Container(content=ft.Column([
                ip_telefono,
                ft.Container(),
                ip_paciente
            ]
            ), width=300, 
            #margin=ft.margin.only(left=10, top=10, right=10), 
            #border=ft.border.all()
            )
               
        col_edad=ft.Container(content=ft.Column([
                ip_edad
            ]
            ), width=300, 
            #border=ft.border.all()
            )

        col_genero=ft.Container(content=ft.Column([
                ip_genero,
            ]
            ), width=300, 
            #border=ft.border.all()
            )
        col_trabajo=ft.Container(content=ft.Column([
                txt_trabajo,
                ip_trabajo
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )
        col_valid_trabajo=ft.Container(content=ft.Row([
                icon_valid_trabajo,
                txt_valid_trabajo    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        col_hipertension=ft.Container(content=ft.Column([
                txt_hipertension,
                ip_hipertension
            ],horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ), width=300, 
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all(),
            )
        col_valid_hipertension=ft.Container(content=ft.Row([
                icon_valid_hipertension,
                txt_valid_hipertension    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        col_cardiopatia=ft.Container(content=ft.Column([
                txt_cardiopatia,
                ip_cardiopatia
            ],horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10, 
            #border=ft.border.all()
            )
        col_valid_cardiopatia=ft.Container(content=ft.Row([
                icon_valid_cardiopatia,
                txt_valid_cardiopatia    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        col_fumador=ft.Container(content=ft.Column([
                txt_fumador,
                ip_fumador
            ]
            ), width=300, 
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10
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
        col_glucosa=ft.Container(content=ft.Column([
                ip_glucosa
            ]
            ), width=300,
            #border=ft.border.all()
            )
        col_valid_glucosa=ft.Container(content=ft.Row([
                icon_valid_glucosa,
                txt_valid_glucosa    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        col_imc=ft.Container(content=ft.Column([
                ip_imc
            ]
            ), width=300,
            #border=ft.border.all()
            )
        col_valid_imc=ft.Container(content=ft.Row([
                icon_valid_imc,
                txt_valid_imc    
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
        col_resultado=ft.Container(content=ft.ListView([
                prediccion_resultado
            ]
            ), width=300,
            height=300, 
            margin=ft.margin.only(left=10,bottom=10,right=10),
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
        row_trabajo=ft.Container(content=ft.Column([
                col_trabajo,
                col_valid_trabajo
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )
        row_hipertension=ft.Container(content=ft.Column([
                col_hipertension,
                col_valid_hipertension
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )
        row_cardiopatia=ft.Container(content=ft.Column([
                col_cardiopatia,
                col_valid_cardiopatia
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )
        row_glucosa=ft.Container(content=ft.Column([
                col_glucosa,
                col_valid_glucosa
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )
        row_imc=ft.Container(content=ft.Column([
                col_imc,
                col_valid_imc
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_fumador=ft.Container(content=ft.Column([
                col_fumador,
                col_valid_fumador
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center,
        #border=ft.border.all(),
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
        ), 
        bgcolor=color_primary,
        padding=ft.padding.only(left=20, top=10, bottom=20, right=20),
        )

        row_form=ft.Container(content=ft.Column([
                row_titulo_form,
                row_paciente,
                row_edad,
                #ft.Container(height=1, width=300, margin=20, bgcolor='#cccccc'),
                row_genero,
                row_trabajo,
                row_hipertension,
                row_cardiopatia,
                row_fumador,
                row_glucosa,
                row_imc,
                row_boton,
                row_resultado],
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
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
        )

        #page.controls.clear()
        page.controls.append(objetive1_scrollable)
        page.update()



