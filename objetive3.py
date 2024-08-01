import flet as ft
import requests

#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 2
def objetive3_view(page, app_state):
        global prediccion_resultado        
        API_URL = 'http://127.0.0.1:8080/api/acv2'

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
                "Genero": ip_genero.value,
                "Edad": ip_edad.value,
                "TipoTrabajo": ip_trabajo.value,  # Actualizado
                "Hipertension": ip_hipertension.value,  # Actualizado
                "Cardiopatia": ip_cardiopatia.value,  # Actualizado
                "Nivel_GlucosaPromedio": ip_glucosa.value,  # Actualizado
                "ICM": ip_imc.value,  # Actualizado
            }
            
            if not datos["Nombre del paciente"]:
                prediccion_resultado.value = "Error: El nombre del paciente es obligatorio."
                page.update()
                return

            if not datos["Edad"]:
                prediccion_resultado.value = "Error: La edad es obligatorio."
                page.update()
                return
            
            if not datos["Genero"]:
                prediccion_resultado.value = "Error: El género es obligatorio."
                page.update()
                return
            
            # Asegúrate de que todos los dropdowns tengan un valor seleccionado
            for campo in ["TipoTrabajo", "Hipertension", "Cardiopatia"]:
                if datos[campo] not in ["1", "2", "3", "4", "0"]:
                    prediccion_resultado.value = f"Error: El campo '{campo}' es obligatorio y debe ser válido."
                    page.update()
                    return

            # Validar que los campos de número no estén vacíos y sean números
            for campo in ["Nivel_GlucosaPromedio", "ICM"]:
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

            if not validar_numero(ip_edad.value, 1, 120):
                errores.append("La edad debe ser un número entre 1 y 120.")
            
            if not validar_numero(ip_glucosa.value, 30, 300):
                errores.append("El nivel de glucosa debe ser un número entre 30 y 300.")
            
            if not validar_numero(ip_imc.value, 10, 100):
                errores.append("El IMC debe ser un número entre 10 y 100.")
                
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

                    if prediction_value == 2:
                        mensaje = "Predicción: Pertenece al grupo de precaución mayor"
                    elif prediction_value == 0:
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

        #titulo del objetivo 2
        txt_objetivo = ft.Text("Segmentación de pacientes", style=ft.TextStyle(size=20, weight="bold", color=ft.colors.WHITE))
        
        #breve descripcion del tema
        txt_descripcion = ft.Text("Clasificados bajo estilo de vida", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
        imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj2.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,)
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

        #input para la edad
        ip_edad=ft.TextField(
            label="Edad",
            keyboard_type="number",
            prefix_icon=ft.icons.CALENDAR_MONTH,
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

        #input para el genero
        ip_genero=ft.Dropdown(
            label="Género",
            hint_text="Seleccionar un género",
            prefix_icon=ft.icons.MALE,
            options=[
                ft.dropdown.Option("0", "Femenino"),
                ft.dropdown.Option("1", "Masculino")
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

                #input para la hipertencion
        ip_hipertension=ft.Dropdown(
            label="Hipertensión",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
            options=[
                ft.dropdown.Option("0", "No"),
                ft.dropdown.Option("1", "Sí")
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
            focused_border_color=ft.colors.BLUE_300,
            bgcolor=ft.colors.WHITE,
            border_color="#dddddd")

        #input para la cardiopatia
        ip_cardiopatia=ft.Dropdown(
            label="Cardiopatía",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
            options=[
                ft.dropdown.Option("0", "No"),
                ft.dropdown.Option("1", "Sí")
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
            focused_border_color=ft.colors.BLUE_300,
            bgcolor=ft.colors.WHITE,
            border_color="#dddddd")

        #input para el nivel de glucosa promedio
        ip_glucosa=ft.TextField(
            label="Nivel de Glucosa Promedio",
            keyboard_type="number",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
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

        #input para el IMC
        ip_imc= ft.TextField(
            label="ICM",
            keyboard_type="number",
            prefix_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
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
        
                #input para el tipo de trabajo
        ip_trabajo=ft.Dropdown(
            label="Tipo de Trabajo",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.WORK_OUTLINE,
            options=[
                ft.dropdown.Option("0", "Trabajador para el gobierno"),
                ft.dropdown.Option("1", "Nunca trabajó"),
                ft.dropdown.Option("2", "Trabajador privado"),
                ft.dropdown.Option("3", "Trabajador por cuenta propia"),
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
            focused_border_color=ft.colors.BLUE_300,
            bgcolor=ft.colors.WHITE,
            border_color="#dddddd")

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
        txt_sub_resultado= ft.Text("Resultado Obtenido por factores médicos:", style=ft.TextStyle(size=16, color="#333333"))

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
        
        col_edad=ft.Container(content=ft.Column([
                ip_edad
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )

        col_genero=ft.Container(content=ft.Column([
                ip_genero
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )

        col_hipertension=ft.Container(content=ft.Column([
                ip_hipertension
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        col_cardiopatia=ft.Container(content=ft.Column([
                ip_cardiopatia
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        col_glucosa=ft.Container(content=ft.Column([
                ip_glucosa
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        col_imc=ft.Container(content=ft.Column([
                ip_imc
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        
        col_trabajo=ft.Container(content=ft.Column([
                ip_trabajo
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )
        
        col_boton=ft.Container(content=ft.Column([
                btn_diagnosticar
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
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

        row_edad=ft.Container(content=ft.Column([
                col_edad
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_genero=ft.Container(content=ft.Column([
                col_genero
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )

        row_hipertension=ft.Container(content=ft.Column([
                col_hipertension]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_cardiopatia=ft.Container(content=ft.Column([
                col_cardiopatia]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_glucosa=ft.Container(content=ft.Column([
                col_glucosa]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_imc=ft.Container(content=ft.Column([
                col_imc]
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_trabajo=ft.Container(content=ft.Column([
                col_trabajo
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
                row_hipertension,
                row_cardiopatia,
                row_glucosa,
                row_imc,
                row_trabajo,
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

        objetive2_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
    )

        page.controls.clear()
        page.controls.append(objetive2_scrollable)
        page.update()
