import flet as ft


#VISTA DE PREDICCIÓN DE DIAGNÓSTICO - OBJETIVO 2
def objetive2_view(page, app_state):
        page.controls.clear()
        page.padding=0
        #----------------------------------------------------------------------------------------------------------------------------------------------
        
        #MÉTODOS    
        def accion_volver_home(e):
            page.controls.clear()
            app_state.show_home()
            page.update()

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
