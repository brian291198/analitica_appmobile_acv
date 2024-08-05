import flet as ft
import requests

#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 3
def objetive2_view(page, app_state):
        global prediccion_resultado        
        API_URL = 'http://127.0.0.1:8000/api/acv3'

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
            
            if not datos["Nombre del paciente"]:
                prediccion_resultado.value = "Error: El nombre del paciente es obligatorio."
                page.update()
                return
            
            if not datos["horasDormidas"]:
                prediccion_resultado.value = "Error: Horas dormidas es un campo obligatorio."
                page.update()
                return
            
            # Asegúrate de que todos los dropdowns tengan un valor seleccionado
            for campo in ["edadRango", "genero", "etnia", "fumador", "bebedorFrecuente", "actividadFisica"]:
                if datos[campo] not in ["1", "2", "3", "4", "0"]:
                    prediccion_resultado.value = f"Error: El campo '{campo}' es obligatorio y debe ser válido."
                    page.update()
                    return

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
        txt_descripcion = ft.Text("Clasificados bajo factores médicos", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
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
#input para fumador frecuente
        ip_fumador=ft.Dropdown(
            label="¿Fumador frecuente?",
            hint_text="Seleccionar opcion",
            prefix_icon=ft.icons.SMOKING_ROOMS,
            options=[
                ft.dropdown.Option("0", "No"),
                ft.dropdown.Option("1", "Si")
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

        #input para bebedor frecuente
        ip_bebedor=ft.Dropdown(
            label="¿Bebedor frecuente?",
            hint_text="Seleccionar opcion",
            prefix_icon=ft.icons.LIQUOR,
            options=[
                ft.dropdown.Option("0", "No"),
                ft.dropdown.Option("1", "Si")
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

        #input para actividad física frecuente
        ip_fisica=ft.Dropdown(
            label="¿Actividad física frecuente?",
            hint_text="Seleccionar opcion",
            prefix_icon=ft.icons.DIRECTIONS_RUN,
            options=[
                ft.dropdown.Option("0", "No"),
                ft.dropdown.Option("1", "Si")
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

        #input para rango de edad
        ip_edad=ft.Dropdown(
            label="Rango de edad",
            hint_text="Seleccionar opcion",
            prefix_icon=ft.icons.CALENDAR_MONTH,
            options=[
                    ft.dropdown.Option("0", "18-24"),
                    ft.dropdown.Option("1", "25-29"),
                    ft.dropdown.Option("2", "30-34"),
                    ft.dropdown.Option("3", "35-39"),
                    ft.dropdown.Option("4", "40-44"),
                    ft.dropdown.Option("5", "45-49"),
                    ft.dropdown.Option("6", "50-54"),
                    ft.dropdown.Option("7", "55-59"),
                    ft.dropdown.Option("8", "60-64"),
                    ft.dropdown.Option("9", "65-69"),
                    ft.dropdown.Option("10", "70-74"),
                    ft.dropdown.Option("11", "75-79"),
                    ft.dropdown.Option("12", "80 a más"),
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
        
        col_fumador=ft.Container(content=ft.Column([
                ip_fumador
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )

        col_bebedor=ft.Container(content=ft.Column([
                ip_bebedor
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )

        col_fisica=ft.Container(content=ft.Column([
                ip_fisica
            ]
            ), width=300, 
            margin=10, 
            #border=ft.border.all()
            )

        col_horas=ft.Container(content=ft.Column([
                ip_horas
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

        col_etnia=ft.Container(content=ft.Column([
                ip_etnia
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
              col_genero
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
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