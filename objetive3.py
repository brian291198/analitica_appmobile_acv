import flet as ft
import requests

#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 3
def objetive3_view(page, app_state):
        global prediccion_resultado        
        API_URL = 'http://127.0.0.1:8080/api/acv3'

        page.controls.clear()
        page.padding=0
        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #MÉTODOS    
        def accion_volver_home(e):
            page.controls.clear()
            app_state.show_home()
            page.update()

        def diagnosticar(e):
            # Recoger los valores de los campos del formulario
            datos = {
                "Nombre del paciente": ip_paciente.value,
                "edadRango": ip_edad.value,
                "genero": ip_genero.value,
                "etnia": ip_etnia.value,
                "fumador": ip_fumador.value,
                "bebedorFrecuente": ip_bebedor.value,
                "actividadFisica": ip_fisica.value,
                "horasDormidas": ip_horas.value,
                
            }
            
            #Método para crear la alerta en un modal
            def create_alert_dialog():
                return ft.AlertDialog(
                title=ft.Column(
                controls=[
                    ft.Text("Datos Incompletos", color=ft.colors.RED, text_align=ft.TextAlign.CENTER, size=20),
                    ft.Container(height=1, width=350, margin=10, bgcolor=ft.colors.RED),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                #on_dismiss=lambda e: page.add(ft.Text("Mensaje auxiliar")),
                bgcolor=ft.colors.WHITE, 
                shadow_color=ft.colors.SECONDARY,
                shape=ft.RoundedRectangleBorder(10)
                )
            page.update()
            
            #Método para agregar el texto de las validaciones que mostrará el modal
            def open_alert(content_text):
                global alerta_validaciones
                alerta_validaciones.content = ft.Text(content_text, color=ft.colors.RED)
                page.open(alerta_validaciones)
                #page.dialog_open = True
                page.update()           

            errores=[]
            
            #Estilo estándar error
            def style_standar_error_vacio(col_valid, txt_valid, icon):
                col_valid.height=40
                txt_valid.value= "Error: Campo obligatorio."
                txt_valid.color=ft.colors.RED_300
                txt_valid.size=12
                icon.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon.color=ft.colors.RED_300
                icon.size=15
            
            #Estilos para error por campo vacío para textfields
            def style_vacio_textfield(col_valid, ip, txt_valid, icon):
                ip.border_color = ft.colors.RED_300
                ip.focused_border_color = ft.colors.RED_300 
                style_standar_error_vacio(col_valid, txt_valid, icon)
            
            #Estilos para error por campo vacío para radiobuttons 
            def style_vacio_radio(col_valid, col_tipo, txt_valid, icon): 
                col_tipo.border = ft.border.all(color=ft.colors.RED_300) 
                style_standar_error_vacio(col_valid, txt_valid, icon)
                 
                
                   
            # VALIDACIONES PARA CAMPOS VACÍOS   
            if not datos["Nombre del paciente"]:
                # prediccion_resultado.value = "Error: El nombre del paciente es obligatorio."
                errores.append("• Error: Campo 'Nombre del paciente' requerido.")
                style_vacio_textfield(col_valid_paciente, ip_paciente, txt_valid_paciente, icon_valid_paciente)
                
                page.update()
                return
            
            if not datos["horasDormidas"]:
                errores.append("• Error: Campo 'Horas dormidas' requerido.")
                style_vacio_textfield(col_valid_paciente, ip_paciente, txt_valid_paciente, icon_valid_paciente)
                return
            
            # Asegúrate de que todos los dropdowns tengan un valor seleccionado
            if not datos["Genero"]:
                #prediccion_resultado.value = "Error: El género es obligatorio."
                errores.append("• Error: Campo 'Género' requerido.")
                style_vacio_radio(col_valid_genero, col_genero, txt_valid_genero, icon_valid_genero)
            
            # Validar que los campos de número no estén vacíos y sean números
            for campo in ["horasDormidas"]:
                if not datos[campo].replace('.', '', 1).isdigit():
                    prediccion_resultado.value = f"Error: El campo '{campo}' debe ser un número válido."
                    page.update()
                    return

            def validar_numero(valor, min_valor, max_valor):
                try:
                    numero = float(valor)
                    if min_valor <= numero <= max_valor:
                        return True
                    return False
                except ValueError:
                    return False
                
            errores = []

            if not validar_numero(ip_horas.value, 1, 20):
                errores.append("La edad debe ser un número entre 1 y 20.")

            if errores:
                prediccion_resultado.value = "\n".join(errores)
                page.update()
                return

            # Imprimir los datos en la consola
            print(datos)

            # Enviar una solicitud POST a la API
            try:
                headers = {'Content-Type': 'application/json'}
                response = requests.post(API_URL, json=datos, headers=headers)
                if response.status_code == 200:
                    # Manejar la respuesta exitosa
                    response_json = response.json()
                    prediction_value = response_json.get('prediction', [0])[0]
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
        
        #VALIDACIONES COMPLETAS POR CAMPO

        def validate_ip_paciente(e):
            input_value = e.control.value
            if not input_value:
                col_valid_paciente.height=40
                txt_valid_paciente.value= "Error: Campo obligatorio."
                txt_valid_paciente.color=ft.colors.RED_300
                txt_valid_paciente.size=12
                ip_paciente.border_color = ft.colors.RED_300
                ip_paciente.focused_border_color = ft.colors.RED_300
                icon_valid_paciente.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_paciente.color=ft.colors.RED_300
                icon_valid_paciente.size=15
            elif all(c.isalpha() or c.isspace() for c in input_value):
                col_valid_paciente.height=40
                txt_valid_paciente.value= "Campo válido"
                txt_valid_paciente.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_paciente.size=12
                ip_paciente.border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                ip_paciente.focused_border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_paciente.name=name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_paciente.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_paciente.size=15
            else:
                col_valid_paciente.height=40
                txt_valid_paciente.value= "Error: Incluir solo letras y espacios."
                txt_valid_paciente.color=ft.colors.RED_300
                txt_valid_paciente.size=12
                ip_paciente.border_color = ft.colors.RED_300
                ip_paciente.focused_border_color = ft.colors.RED_300
                icon_valid_paciente.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_paciente.color=ft.colors.RED_300
                icon_valid_paciente.size=15
            page.update()

        def validate_ip_edad(e):
            input_value = e.control.value
            # Intentar convertir la entrada a un número entero
            try:
                age = int(input_value)
            except ValueError:
                age = None

            if not input_value:
                col_valid_edad.height=40
                txt_valid_edad.value= "Error: Campo obligatorio."
                txt_valid_edad.color=ft.colors.RED_300
                txt_valid_edad.size=12
                ip_edad.border_color = ft.colors.RED_300
                ip_edad.focused_border_color = ft.colors.RED_300
                icon_valid_edad.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_edad.color=ft.colors.RED_300
                icon_valid_edad.size=15
            elif age is None or not (1 <= age <= 120):
                col_valid_edad.height=40
                txt_valid_edad.value= "Error: Ingrese una edad entre 1 y 120."
                txt_valid_edad.color=ft.colors.RED_300
                txt_valid_edad.size=12
                ip_edad.border_color = ft.colors.RED_300
                ip_edad.focused_border_color = ft.colors.RED_300
                icon_valid_edad.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_edad.color=ft.colors.RED_300
                icon_valid_edad.size=15
            else:
                col_valid_edad.height=40
                txt_valid_edad.value= "Campo válido"
                txt_valid_edad.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_edad.size=12
                ip_edad.border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                ip_edad.focused_border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_edad.name=name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_edad.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_edad.size=15
            page.update()

        def validate_ip_genero(e):
            input_value = e.control.value

            if not input_value:
                col_valid_genero.height=40
                txt_valid_genero.value= "Error: Campo obligatorio."
                txt_valid_genero.color=ft.colors.RED_300
                txt_valid_genero.size=12
                col_genero.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_genero.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_genero.color=ft.colors.RED_300
                icon_valid_genero.size=15
            else:
                col_valid_genero.height=40
                txt_valid_genero.value= "Campo válido"
                txt_valid_genero.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_genero.size=12
                col_genero.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_genero.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_genero.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_genero.size=15
            page.update()
 
        
        def validate_ip_etnia(e):
            input_value = e.control.value

            if not input_value:
                col_valid_etnia.height=40
                txt_valid_etnia.value= "Error: Campo obligatorio."
                txt_valid_etnia.color=ft.colors.RED_300
                txt_valid_etnia.size=12
                col_etnia.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_etnia.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_etnia.color=ft.colors.RED_300
                icon_valid_etnia.size=15
            else:
                col_valid_etnia.height=40
                txt_valid_etnia.value= "Campo válido"
                txt_valid_etnia.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_etnia.size=12
                col_etnia.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_etnia.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_etnia.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_etnia.size=15
            page.update()
        
        def validate_ip_fumador(e):
            input_value = e.control.value

            if not input_value:
                col_valid_fumador.height=40
                txt_valid_fumador.value= "Error: Campo obligatorio."
                txt_valid_fumador.color=ft.colors.RED_300
                txt_valid_fumador.size=12
                col_fumador.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_fumador.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_fumador.color=ft.colors.RED_300
                icon_valid_fumador.size=15
            else:
                col_valid_fumador.height=40
                txt_valid_fumador.value= "Campo válido"
                txt_valid_fumador.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_fumador.size=12
                col_fumador.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_fumador.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_fumador.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_fumador.size=15
            page.update()
        def validate_ip_bebedor(e):
            input_value = e.control.value

            if not input_value:
                col_valid_bebedor.height=40
                txt_valid_bebedor.value= "Error: Campo obligatorio."
                txt_valid_bebedor.color=ft.colors.RED_300
                txt_valid_bebedor.size=12
                col_bebedor.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_bebedor.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_bebedor.color=ft.colors.RED_300
                icon_valid_bebedor.size=15
            else:
                col_valid_bebedor.height=40
                txt_valid_bebedor.value= "Campo válido"
                txt_valid_bebedor.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_bebedor.size=12
                col_bebedor.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_bebedor.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_bebedor.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_bebedor.size=15
            page.update()
        
        def validate_ip_fisica(e):
            input_value = e.control.value

            if not input_value:
                col_valid_fisica.height=40
                txt_valid_fisica.value= "Error: Campo obligatorio."
                txt_valid_fisica.color=ft.colors.RED_300
                txt_valid_fisica.size=12
                col_fisica.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_fisica.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_fisica.color=ft.colors.RED_300
                icon_valid_fisica.size=15
            else:
                col_valid_fisica.height=40
                txt_valid_fisica.value= "Campo válido"
                txt_valid_fisica.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_fisica.size=12
                col_fisica.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_fisica.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_fisica.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_fisica.size=15
            page.update()
            
        def validate_ip_horas(e):
            input_value = e.control.value

            if not input_value:
                col_valid_horas.height=40
                txt_valid_horas.value= "Error: Campo obligatorio."
                txt_valid_horas.color=ft.colors.RED_300
                txt_valid_horas.size=12
                col_horas.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_horas.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_horas.color=ft.colors.RED_300
                icon_valid_horas.size=15
            else:
                col_valid_horas.height=40
                txt_valid_horas.value= "Campo válido"
                txt_valid_horas.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_horas.size=12
                col_horas.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_horas.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_horas.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_horas.size=15
            page.update()
        
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

        #boton en texto -> < VOLVER
        texto_volver = ft.TextButton(
            on_click=accion_volver_home,
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
        txt_descripcion = ft.Text("Clasificados bajo estilo de vida", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
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
            border_color="#cccccc",
            on_change=validate_ip_paciente
        )
        #texto para validacion de campo ip_paciente
        txt_valid_paciente=ft.Text()

        #input para el Estado de Fumador
        txt_fumador=ft.Row(
            [
                ft.Icon(name=ft.icons.SMOKING_ROOMS, color="#333333"),
                ft.Text("Fumador", color="#333333")
            ]
        )        
        ip_fumador = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Si",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )), 
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_fumador)
        
        #texto para validacion de campo ip_fumador
        txt_valid_fumador=ft.Text()
        
        #input para bebedor frecuente
               
        txt_bebedor=ft.Row(
            [
                ft.Icon(name=ft.icons.LIQUOR, color="#333333"),
                ft.Text("¿Bebedor frecuente?", color="#333333")
            ]
        )        
        ip_bebedor = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Si",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )), 
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_bebedor)
        
        #texto para validacion de campo ip_fumador
        txt_valid_bebedor=ft.Text()
         
        
        txt_fisica=ft.Row(
            [
                ft.Icon(name=ft.icons.DIRECTIONS_RUN, color="#333333"),
                ft.Text("¿Actividad física frecuente?", color="#333333")
            ]
        )        
        ip_fisica = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Si",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )), 
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_fisica)
        
        #texto para validacion de campo ip_fumador
        txt_valid_fisica=ft.Text()

        #input para horas dormidas
        ip_horas=ft.TextField(
            label="Horas dormidas",
            keyboard_type="number",
            prefix_icon=ft.icons.HOTEL,
            hint_text="0",
            content_padding=0,
            color="#333333",
            hint_style=ft.TextStyle(
                color="#dddddd",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color="#dddddd",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            selection_color="#333333",
            prefix_style=ft.TextStyle(
                bgcolor=ft.colors.BLACK,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            cursor_color="#333333",
            fill_color=ft.colors.WHITE,
            focused_border_color=ft.colors.BLUE_300,
            border_color="#dddddd"
        )
        
        txt_valid_horas=ft.Text()

        #input para la edad
        ip_edad=ft.TextField(
            label="Edad",
            keyboard_type="number",
            prefix_icon=ft.icons.CALENDAR_MONTH,
            hint_text="0",
            content_padding=0,
            color="#333333",
            hint_style=ft.TextStyle(
                color="#cccccc",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color="#cccccc",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            selection_color="#333333",
            prefix_style=ft.TextStyle(
                bgcolor=ft.colors.BLACK,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            cursor_color="#333333",
            fill_color=ft.colors.WHITE,
            focused_border_color=ft.colors.BLUE_300,
            border_color="#cccccc",
            on_change=validate_ip_edad
        )
        #texto para validacion de campo ip_edad
        txt_valid_edad=ft.Text() 
        
        #input para el genero
        txt_genero=ft.Row(
            [
                ft.Icon(name=ft.icons.MALE, color="#333333"),
                ft.Text("Género", color="#333333")
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ])
        ip_genero = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="Femenino",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Masculino",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_genero 
            )
        #texto para validacion de campo ip_genero
        txt_valid_genero=ft.Text()

        #input para la etnia
        ip_etnia=ft.Dropdown(
            label="Etnia",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.DIVERSITY_3,
            options=[
                    ft.dropdown.Option("0", "Indígena"),
                    ft.dropdown.Option("1", "Asiático"),
                    ft.dropdown.Option("2", "Negro"),
                    ft.dropdown.Option("3", "Hispano"),
                    ft.dropdown.Option("4", "Blanco"),
                    ft.dropdown.Option("4", "Otro"),
            ],
            content_padding=0,
            color="#333333",
            hint_style=ft.TextStyle(
                color="#dddddd",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color="#dddddd",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            prefix_style=ft.TextStyle(
                bgcolor=ft.colors.BLACK,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            bgcolor=ft.colors.WHITE,
            focused_border_color=ft.colors.BLUE_300,
            border_color="#dddddd"
        )
        
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
                    ft.ControlState.HOVERED: ft.colors.BLUE_300,
                    ft.ControlState.DEFAULT: ft.colors.BLUE_600,
                },
            )
            )

        #etiqueta -> Obtener resultado
        txt_sub_resultado= ft.Text("Resultado Obtenido por factores de calidad de vida:", style=ft.TextStyle(size=16, color="#333333"))

        #text, para mostrar el resultado de predicción
        prediccion_resultado=ft.Text("Resultado...", style=ft.TextStyle(size=15, color=ft.colors.BLUE_600))

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
            margin=10, 
            #border=ft.border.all()
            )     
        col_valid_paciente=ft.Container(content=ft.Row([
                icon_valid_paciente,
                txt_valid_paciente    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            ) 
        
        col_fumador=ft.Container(content=ft.Column([
                ip_fumador
            ]
            ), width=300, 
            margin=10, 
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
                ip_bebedor
            ]
            ), width=300, 
            margin=10,  
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
                ip_fisica
            ]
            ), width=300, 
            margin=10, 
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
            margin=10, 
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

        col_edad=ft.Container(content=ft.Column([
                ip_edad
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        col_valid_edad=ft.Container(content=ft.Row([
                icon_valid_edad,
                txt_valid_edad,
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,
        )


        col_genero=ft.Container(content=ft.Column([
                txt_genero,
                ip_genero
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        col_valid_genero=ft.Container(content=ft.Row([
                icon_valid_genero,
                txt_valid_genero    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        
        col_etnia=ft.Container(content=ft.Column([
                ip_etnia
            ]
            ), width=300, 
            margin=10, 
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
                txt_sub_resultado,
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
        bgcolor=ft.colors.BLUE_600,
        width=360,
        border=None,
        )
        row_titulo_container=ft.Container(content=ft.Row([
              col_derecha,
              col_izquierda
        ]
        ), 
        bgcolor=ft.colors.BLUE_600,
        width=360,
        alignment=ft.alignment.center,
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
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_fumador=ft.Container(content=ft.Column([
              col_fumador
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_bebedor=ft.Container(content=ft.Column([
              col_bebedor
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_fisica=ft.Container(content=ft.Column([
              col_fisica
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_horas=ft.Container(content=ft.Column([
              col_horas
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_edad=ft.Container(content=ft.Column([
              col_edad
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_genero=ft.Container(content=ft.Column([
              col_genero,
              col_valid_genero
        ], spacing = 0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center, 
        )

        row_etnia=ft.Container(content=ft.Column([
              col_etnia
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
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
              col_resultado
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
              
        ],spacing=0,
        ), bgcolor=ft.colors.BLUE_600, padding=20,
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
              margin=15,
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

        page.controls.clear()
        page.controls.append(objetive3_scrollable)
        page.update()