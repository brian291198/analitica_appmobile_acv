import flet as ft


#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 1
def objetive1_view(page, app_state):
        page.controls.clear()
        page.padding=0

        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #MÉTODOS    
        def accion_volver_home(e):
            page.controls.clear()
            app_state.show_home()
            page.update()
        
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
                color="#dddddd",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            label_style=ft.TextStyle(
                color="#dddddd",  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            selection_color="#333333",
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

        #input para el tipo de trabajo
        ip_trabajo=ft.Dropdown(
            label="Tipo de Trabajo",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.WORK,
            options=[
                ft.dropdown.Option("1", "Trabajador por cuenta propia"),
                ft.dropdown.Option("2", "Trabajador para el gobierno"),
                ft.dropdown.Option("3", "Nunca trabajó"),
                ft.dropdown.Option("4", "Trabajador privado")
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
        
        #input para la hipertencion
        ip_hipertension=ft.Dropdown(
            label="Hipertensión",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.MEDICATION_ROUNDED,
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
            prefix_icon=ft.icons.MEDICATION_ROUNDED,
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
            prefix_icon=ft.icons.MEDICATION_ROUNDED,
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
            prefix_icon=ft.icons.MEDICATION_ROUNDED,
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
        
        #input para el Estado de Fumador
        ip_fumador= ft.Dropdown(
            label="Estado de Fumador",
            hint_text="Seleccionar opción",
            prefix_icon=ft.icons.MEDICATION_ROUNDED,
            options=[
                ft.dropdown.Option("1", "Anteriormente fumó"),
                ft.dropdown.Option("2", "Nunca fumó"),
                ft.dropdown.Option("3", "Fuma")
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
            text="Diagnosticar",
            width=300, 
            height=40,  
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
        txt_sub_resultado= ft.Text("Resultado Obtenido:", style=ft.TextStyle(size=16, color="#333333"))

        #text, para mostrar el resultado de predicción
        prediccion_resultado=ft.Text("Resultado...", style=ft.TextStyle(size=12, color=ft.colors.BLUE_600))

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
        col_genero=ft.Container(content=ft.Column([
                ip_genero
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
        col_trabajo=ft.Container(content=ft.Column([
                ip_trabajo
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
        col_fumador=ft.Container(content=ft.Column([
                ip_fumador
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
              col_paciente
        ]
        ),
        alignment=ft.alignment.center, 
        #border=ft.border.all()
        )
        row_genero=ft.Container(content=ft.Column([       
              col_genero]
        ), 
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

        row_edad=ft.Container(content=ft.Column([         
              col_edad]
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

        row_fumador=ft.Container(content=ft.Column([
              col_fumador]
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
        ), 
        bgcolor=ft.colors.BLUE_600,
        padding=20,
        )

        row_form=ft.Container(content=ft.Column([
              row_titulo_form,
              row_paciente,
              row_genero,
              row_edad,
              row_trabajo,
              ft.Container(height=1, width=300, margin=20, bgcolor='#dddddd'),
              row_hipertension,
              row_cardiopatia,
              row_glucosa,
              row_imc,
              row_fumador,
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



        """ page.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Formulario de Predicción", style=ft.TextStyle(size=20, weight="bold", color="#333333")),
                    
                    
                    # Botones
                    ft.Column([
                        ft.ElevatedButton(text="Guardar"),
                        ft.ElevatedButton(text="Regresar")
                    ], spacing=10, alignment="center")
                ],
                spacing=10,
                alignment="center",
                width=page.window_width * 0.8,  # 90% del ancho de la ventana
                auto_scroll=True 
         
            )
        )
      
        page.update()  """  