import flet as ft
import requests
from message_whatsapp import message_whatsapp
from login import login_view



#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 1
def objetive1_view(page, app_state):
        if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return

        global prediccion_resultado  
        API_URL = 'http://127.0.0.1:8080/api/acv1'

        page.controls.clear()
        page.padding=0
        
        #----------------------------------------------------------------------------------------------------------------------------------------------
       
        #MÉTODOS    
        def accion_volver_home(e):
            page.controls.clear()
            app_state.show_home()
            page.update()
        
        def diagnosticar(e):
            global alerta_validaciones
            # Recoger los valores de los campos del formulario
            datos = {
                "Nombre del paciente": ip_paciente.value,
                "Genero": ip_genero.value,  # Actualizado
                "Edad": ip_edad.value,
                "Hipertension": ip_hipertension.value,  # Actualizado
                "Cardiopatia": ip_cardiopatia.value,  # Actualizado
                "TipoTrabajo": ip_trabajo.value,  # Actualizado
                "Nivel_GlucosaPromedio": ip_glucosa.value,  # Actualizado
                "ICM": ip_imc.value,  # Actualizado
                "EstadoFumador": ip_fumador.value,  # Actualizado
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

            #Estilos para error por campo vacío para textfields
            def style_vacio_textfield(col_valid, ip, txt_valid, icon):
                col_valid.height=40
                ip.border_color = ft.colors.RED_300
                ip.focused_border_color = ft.colors.RED_300
                txt_valid.value= "Error: Campo obligatorio."
                txt_valid.color=ft.colors.RED_300
                txt_valid.size=12
                icon.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon.color=ft.colors.RED_300
                icon.size=15

            #Estilos para error por campo vacío para radiobuttons
            def style_vacio_radio(col_valid, col_tipo, txt_valid, icon):
                col_valid.height=40
                col_tipo.border = ft.border.all(color=ft.colors.RED_300)
                txt_valid.value= "Error: Campo obligatorio."
                txt_valid.color=ft.colors.RED_300
                txt_valid.size=12
                icon.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon.color=ft.colors.RED_300
                icon.size=15
                                
            # VALIDACIONES PARA CAMPOS VACÍOS
            if not datos["Nombre del paciente"]:
                #prediccion_resultado.value = "Error: El nombre del paciente es obligatorio."
                errores.append("• Error: Campo 'Nombre del paciente' requerido.")
                style_vacio_textfield(col_valid_paciente, ip_paciente, txt_valid_paciente, icon_valid_paciente)
            
            if not datos["Edad"]:
                #prediccion_resultado.value = "Error: La edad es obligatorio."
                errores.append("• Error: Campo 'Edad' requerido.")
                style_vacio_textfield(col_valid_edad, ip_edad, txt_valid_edad, icon_valid_edad)
               
            if not datos["Genero"]:
                #prediccion_resultado.value = "Error: El género es obligatorio."
                errores.append("• Error: Campo 'Género' requerido.")
                style_vacio_radio(col_valid_genero, col_genero, txt_valid_genero, icon_valid_genero)
            
            if not datos["TipoTrabajo"]:
                errores.append("• Error: Campo 'Tipo de trabajo' requerido.")
                style_vacio_radio(col_valid_trabajo, col_trabajo, txt_valid_trabajo, icon_valid_trabajo)

            if not datos["Hipertension"]:
                errores.append("• Error: Campo 'Hipertensión' requerido.")
                style_vacio_radio(col_valid_hipertension, col_hipertension, txt_valid_hipertension, icon_valid_hipertension)

            if not datos["Cardiopatia"]:
                errores.append("• Error: Campo 'Cardiopatía' requerido.")
                style_vacio_radio(col_valid_cardiopatia, col_cardiopatia, txt_valid_cardiopatia, icon_valid_cardiopatia)
                
            if not datos["EstadoFumador"]:
                errores.append("• Error: Campo 'Estado Fumador' requerido.")
                style_vacio_radio(col_valid_fumador, col_fumador, txt_valid_fumador, icon_valid_fumador)
                            
            if not datos["Nivel_GlucosaPromedio"]:
                errores.append("• Error: Campo 'Glucosa' requerido.")
                style_vacio_textfield(col_valid_glucosa, ip_glucosa, txt_valid_glucosa, icon_valid_glucosa)
            
            if not datos["ICM"]:
                errores.append("• Error: Campo 'IMC' requerido.")
                style_vacio_textfield(col_valid_imc, ip_imc, txt_valid_imc, icon_valid_imc)
                         
            if errores:      
                alerta_validaciones = create_alert_dialog()
                open_alert("\n".join(errores))
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

            if errores:
                #prediccion_resultado.value = "\n".join(errores)
                alerta_validaciones.content.value ="\n".join(errores)
                #alerta_active("\n".join(errores))
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
                        mensaje1="nos complace"
                        mensaje2 = "no presenta riesgo de padecer un accidente cerebrovascular (ACV) en su evaluación actual."
                    else:
                        mensaje1="lamentamos"
                        mensaje2 = "sí presenta riesgo de padecer un accidente cerebrovascular (ACV) en su evaluación actual."

                    prediccion=f"Estimado(a) {ip_paciente.value}, {mensaje1} informarle que, tras evaluar los datos requeridos para el diagnóstico, se determinó que {mensaje2}"
                    prediccion_resultado.value = prediccion

                    #numerito de prueba para enviar el mensaje, incluir el 51 por codigo del pais
                    #telefono='51921351292'
                    telefono=f"51{ip_telefono.value}"

                    message_whatsapp(page, ip_paciente.value, mensaje1, mensaje2, telefono)
                    print(prediccion)                        
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

        def validate_ip_trabajo(e):
            input_value = e.control.value

            if not input_value:
                col_valid_trabajo.height=40
                txt_valid_trabajo.value= "Error: Campo obligatorio."
                txt_valid_trabajo.color=ft.colors.RED_300
                txt_valid_trabajo.size=12
                col_trabajo.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_trabajo.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_trabajo.color=ft.colors.RED_300
                icon_valid_trabajo.size=15
            else:
                col_valid_trabajo.height=40
                txt_valid_trabajo.value= "Campo válido"
                txt_valid_trabajo.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_trabajo.size=12
                col_trabajo.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_trabajo.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_trabajo.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_trabajo.size=15
            page.update()

        def validate_ip_hipertension(e):
            input_value = e.control.value

            if not input_value:
                col_valid_hipertension.height=40
                txt_valid_hipertension.value= "Error: Campo obligatorio."
                txt_valid_hipertension.color=ft.colors.RED_300
                txt_valid_hipertension.size=12
                col_hipertension.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_hipertension.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_hipertension.color=ft.colors.RED_300
                icon_valid_hipertension.size=15
            else:
                col_valid_hipertension.height=40
                txt_valid_hipertension.value= "Campo válido"
                txt_valid_hipertension.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_hipertension.size=12
                col_hipertension.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_hipertension.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_hipertension.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_hipertension.size=15

            page.update()
        def validate_ip_cardiopatia(e):
            input_value = e.control.value

            if not input_value:
                col_valid_cardiopatia.height=40
                txt_valid_cardiopatia.value= "Error: Campo obligatorio."
                txt_valid_cardiopatia.color=ft.colors.RED_300
                txt_valid_cardiopatia.size=12
                col_cardiopatia.border = ft.border.all(color=ft.colors.RED_300)
                icon_valid_cardiopatia.name=name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_cardiopatia.color=ft.colors.RED_300
                icon_valid_cardiopatia.size=15
            else:
                col_valid_cardiopatia.height=40
                txt_valid_cardiopatia.value= "Campo válido"
                txt_valid_cardiopatia.color=ft.colors.LIGHT_GREEN_ACCENT_700
                txt_valid_cardiopatia.size=12
                col_cardiopatia.border = ft.border.all(color=ft.colors.LIGHT_GREEN_ACCENT_700)
                icon_valid_cardiopatia.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                icon_valid_cardiopatia.color=ft.colors.LIGHT_GREEN_ACCENT_700
                icon_valid_cardiopatia.size=15

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

        def validate_ip_glucosa(e):
            input_value = e.control.value
            try:
                # Intentar convertir el valor a flotante
                glucosa_value = float(input_value)
                if not input_value:
                    col_valid_glucosa.height=40
                    txt_valid_glucosa.value= "Error: Campo obligatorio."
                    txt_valid_glucosa.color=ft.colors.RED_300
                    txt_valid_glucosa.size=12
                    ip_glucosa.border_color = ft.colors.RED_300
                    ip_glucosa.focused_border_color = ft.colors.RED_300
                    icon_valid_glucosa.name=ft.icons.ERROR_OUTLINE_ROUNDED
                    icon_valid_glucosa.color=ft.colors.RED_300
                    icon_valid_glucosa.size=15
                elif 30 <= glucosa_value <= 300:
                    col_valid_glucosa.height=40
                    txt_valid_glucosa.value= "Campo válido"
                    txt_valid_glucosa.color=ft.colors.LIGHT_GREEN_ACCENT_700
                    txt_valid_glucosa.size=12
                    ip_glucosa.border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                    ip_glucosa.focused_border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                    icon_valid_glucosa.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                    icon_valid_glucosa.color=ft.colors.LIGHT_GREEN_ACCENT_700
                    icon_valid_glucosa.size=15
                else:
                    col_valid_glucosa.height=40
                    txt_valid_glucosa.value= "Error: Ingrese un valor entre 30 y 300."
                    txt_valid_glucosa.color=ft.colors.RED_300
                    txt_valid_glucosa.size=12
                    ip_glucosa.border_color = ft.colors.RED_300
                    ip_glucosa.focused_border_color = ft.colors.RED_300
                    icon_valid_glucosa.name=ft.icons.ERROR_OUTLINE_ROUNDED
                    icon_valid_glucosa.color=ft.colors.RED_300
                    icon_valid_glucosa.size=15 
            except ValueError:
                col_valid_glucosa.height=40
                txt_valid_glucosa.value= "Error: Solo números enteros o decimales."
                txt_valid_glucosa.color=ft.colors.RED_300
                txt_valid_glucosa.size=12
                ip_glucosa.border_color = ft.colors.RED_300
                ip_glucosa.focused_border_color = ft.colors.RED_300
                icon_valid_glucosa.name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_glucosa.color=ft.colors.RED_300
                icon_valid_glucosa.size=15
            page.update()

        def validate_ip_imc(e):
            input_value = e.control.value
            try:
                # Intentar convertir el valor a flotante
                imc_value = float(input_value)
                if not input_value:
                    col_valid_imc.height=40
                    txt_valid_imc.value= "Error: Campo obligatorio."
                    txt_valid_imc.color=ft.colors.RED_300
                    txt_valid_imc.size=12
                    ip_imc.border_color = ft.colors.RED_300
                    ip_imc.focused_border_color = ft.colors.RED_300
                    icon_valid_imc.name=ft.icons.ERROR_OUTLINE_ROUNDED
                    icon_valid_imc.color=ft.colors.RED_300
                    icon_valid_imc.size=15
                elif 10 <= imc_value <= 100:
                    col_valid_imc.height=40
                    txt_valid_imc.value= "Campo válido"
                    txt_valid_imc.color=ft.colors.LIGHT_GREEN_ACCENT_700
                    txt_valid_imc.size=12
                    ip_imc.border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                    ip_imc.focused_border_color = ft.colors.LIGHT_GREEN_ACCENT_700
                    icon_valid_imc.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
                    icon_valid_imc.color=ft.colors.LIGHT_GREEN_ACCENT_700
                    icon_valid_imc.size=15
                else:
                    col_valid_imc.height=40
                    txt_valid_imc.value= "Error: Ingrese un valor entre 10 y 100."
                    txt_valid_imc.color=ft.colors.RED_300
                    txt_valid_imc.size=12
                    ip_imc.border_color = ft.colors.RED_300
                    ip_imc.focused_border_color = ft.colors.RED_300
                    icon_valid_imc.name=ft.icons.ERROR_OUTLINE_ROUNDED
                    icon_valid_imc.color=ft.colors.RED_300
                    icon_valid_imc.size=15
            except ValueError:
                col_valid_imc.height=40
                txt_valid_imc.value= "Error: Solo números enteros o decimales."
                txt_valid_imc.color=ft.colors.RED_300
                txt_valid_imc.size=12
                ip_imc.border_color = ft.colors.RED_300
                ip_imc.focused_border_color = ft.colors.RED_300
                icon_valid_imc.name=ft.icons.ERROR_OUTLINE_ROUNDED
                icon_valid_imc.color=ft.colors.RED_300
                icon_valid_imc.size=15
            page.update()
           
         #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #ÍCONO PARA VALIDACIONES

        #icon_validation=ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED, color=ft.colors.LIGHT_GREEN_ACCENT_700, size=12)
        #icon_error=ft.Icon(name=ft.icons.ERROR_OUTLINE_ROUNDED, color=ft.colors.RED_300, size=12)
       
        icon_valid_paciente=ft.Icon()            
        icon_valid_edad=ft.Icon()
        icon_valid_genero=ft.Icon()
        icon_valid_trabajo=ft.Icon()
        icon_valid_hipertension=ft.Icon()
        icon_valid_cardiopatia=ft.Icon()
        icon_valid_fumador=ft.Icon()
        icon_valid_glucosa=ft.Icon()
        icon_valid_imc=ft.Icon()

        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #ELEMENTOS DE INTERFAZ
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
            border_color="#cccccc",
        )



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

        #titulo del objetivo 1
        txt_objetivo = ft.Text("Diagnóstico de ACV", style=ft.TextStyle(size=20, weight="bold", color=ft.colors.WHITE))
        
        #breve descripcion del tema
        txt_descripcion = ft.Text("Diagnóstico rápido realizado mediante machine learning", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
        imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj1.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,)
                ]),width=100)
        
        #titulo de formulario
        txt_formulario = ft.Text("Formulario para diagnóstico", style=ft.TextStyle(size=16, color='#333333'))

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

        #input para el tipo de trabajo
        txt_trabajo=ft.Row(
            [
                ft.Icon(name=ft.icons.WORK_OUTLINE, color="#333333"),
                ft.Text("Tipo de Trabajo", color="#333333")
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ]
        )        
        ip_trabajo = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="Trabajador para el gobierno",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Nunca trabajó",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="2", 
                label="Trabajador privado",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="3", 
                label="Trabajador por cuenta propia",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_trabajo)
        
        #texto para validacion de campo ip_trabajo
        txt_valid_trabajo=ft.Text()

        #input para la hipertencion
        txt_hipertension=ft.Row(
            [
                ft.Icon(name=ft.icons.MEDICAL_SERVICES_OUTLINED, color="#333333"),
                ft.Text("Hipertensión", color="#333333")
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ]
        )        
        ip_hipertension = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Sí",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_hipertension)
        
        #texto para validacion de campo ip_hipertension
        txt_valid_hipertension=ft.Text()

        #input para la cardiopatia
        txt_cardiopatia= ft.Row(
            [
                ft.Icon(name=ft.icons.MEDICAL_SERVICES_OUTLINED, color="#333333"),
                ft.Text("Cardiopatía", color="#333333")
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ])

        ip_cardiopatia = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Sí",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_cardiopatia)
        
        #texto para validacion de campo ip_cardiopatia
        txt_valid_cardiopatia=ft.Text()

        #input para el nivel de glucosa promedio
        ip_glucosa=ft.TextField(
            label="Nivel de Glucosa Promedio",
            keyboard_type="number",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
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
            on_change=validate_ip_glucosa
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
            on_change=validate_ip_imc
            )
        
        #texto para validacion de campo ip_imc
        txt_valid_imc=ft.Text()
        
        #input para el Estado de Fumador
        txt_fumador=ft.Row(
            [
                ft.Icon(name=ft.icons.SMOKING_ROOMS, color="#333333"),
                ft.Text("Estado de Fumador", color="#333333")
               # ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
            ]
        )        
        ip_fumador = ft.RadioGroup(content=ft.Column([
            ft.Radio(
                value="0", 
                label="No opina",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="1", 
                label="Anteriormente fumó",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="2", 
                label="Nunca fumó",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ft.Radio(
                value="3", 
                label="Fuma",
                label_style=ft.TextStyle(
                color="#cccccc",
                size=14,
                )),
            ],alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            on_change=validate_ip_fumador)
        
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
                    ft.ControlState.HOVERED: ft.colors.BLUE_300,
                    ft.ControlState.DEFAULT: ft.colors.BLUE_600,
                },
            )
            )

        #etiqueta -> Obtener resultado
        txt_sub_resultado= ft.Text("Resultado Obtenido:", style=ft.TextStyle(size=16, color="#333333"))

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
                ip_telefono,
                ip_paciente
            ]
            ), width=300, 
            #margin=ft.margin.only(left=10, top=10, right=10), 
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
        col_edad=ft.Container(content=ft.Column([
                ip_edad
            ]
            ), width=300, 
            #border=ft.border.all()
            )
        col_valid_edad=ft.Container(content=ft.Row([
                icon_valid_edad,
                txt_valid_edad    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
        col_genero=ft.Container(content=ft.Column([
                txt_genero,
                ip_genero,
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=5, 
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
        col_trabajo=ft.Container(content=ft.Column([
                txt_trabajo,
                ip_trabajo
            ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=5 
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
            border_radius=5 
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
            border_radius=5 
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
            border_radius=5
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
            height=150, 
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
        width=360,
        border=None,
        )
        row_titulo_container=ft.Container(content=ft.Row([
                col_derecha,
                col_izquierda
        ], spacing=0,
        ), 
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
                col_paciente,
                col_valid_paciente
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )
        row_genero=ft.Container(content=ft.Column([       
                col_genero,
                col_valid_genero

        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10), 
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_edad=ft.Container(content=ft.Column([         
                col_edad,
                col_valid_edad
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
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
        ], spacing=0
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
        ), 
        bgcolor=ft.colors.BLUE_600,
        padding=20,
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
        #border=ft.border.all(),
        )
        objetive1_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
        )

        page.controls.clear()
        page.controls.append(objetive1_scrollable)
        page.update()



