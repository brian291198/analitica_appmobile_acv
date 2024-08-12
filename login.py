import flet as ft
import requests
from validation import validate_login
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_check, color_error
import time

def login_view(page, app_state):
    page.bgcolor = ft.colors.WHITE
    API_URL = 'http://localhost:8080/login/'



    overlay = ft.Container(
        width=page.width,
        height=page.height,
        bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),  # Fondo oscuro transparente
        alignment=ft.alignment.center,  # Centrar el contenido (el indicador de carga)
        content=ft.CupertinoActivityIndicator(
            radius=20,
            color=ft.colors.WHITE,
            animating=True,
        ),
        visible=False,  # Inicia oculto
    )

    def ir_register(e):
        page.controls.clear()
        app_state.show_register()
        page.update()

    def handle_login(e):
        username = username_field.value
        password = password_field.value

        datos = {
                "username": username,
                "password": password
            }

        datos_values = [value for key, value in datos.items()]
        datos_keys = [key for key in datos.keys()]

        # Lista para errores
        errores = []
        #Llamada al método para validaciones
        filtro_valid_login(page, datos_values, datos_keys, errores)

        if not errores:
            if not chbx_terminos.value:
                error_alert = ft.AlertDialog(
                    content=ft.Text("Por favor, para continuar debe aceptar los términos y condiciones de uso.", color=color),
                    # actions=[ft.TextButton(text="Aceptar", on_click=lambda e: page.close(error_alert))],
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(10),
                )
                page.open(error_alert)
                page.update()
            else:

                headers = {'Content-Type': 'application/json'}
  
                contenedor_stack.controls.append(overlay)
                overlay.visible=True
                page.update()
                time.sleep(0.5)

                try:
                    response = requests.post(API_URL, json=datos, headers=headers)
                    overlay.visible=False
                    page.update()
                    if response.status_code == 200:
                        #icono de aprobado
                        aprobado = ft.AlertDialog(
                            content=ft.Icon(name=ft.icons.CHECK_CIRCLE_ROUNDED, color=color_check, size=40),
                            bgcolor=ft.colors.TRANSPARENT,)
                        page.open(aprobado)
                        time.sleep(0.5)
                        page.close(aprobado) 
                        page.update() 
                        #obtenere datos
                        response_json = response.json()
                        token = response_json.get('token')
                        user_data = response_json.get('user')
                        paciente_data = response_json.get('paciente')  

                        app_state.token = token
                        app_state.user_data = user_data
                        app_state.paciente_data = paciente_data  

                        # Redirigir a la vista de bienvenida
                        page.controls.clear()
                        app_state.show_welcome()
                        page.update()

                    else:
                        # Mostrar un mensaje de error en la interfaz
                        error_message = response.json().get('message', 'Error desconocido')

                        error_alert = ft.AlertDialog(
                            title=ft.Text("Error de Inicio de Sesión", color=ft.colors.RED_300),
                            content=ft.Text(error_message, color=ft.colors.RED_300),
                            # actions=[ft.TextButton(text="Aceptar", on_click=close_error_dialog)],
                            bgcolor=ft.colors.WHITE,
                            shape=ft.RoundedRectangleBorder(10)
                        )
                        page.open(error_alert)
                        page.update()

                except Exception as e:
                    # Mostrar un mensaje de error en la interfaz
                    error_alert = ft.AlertDialog(
                        title=ft.Text("Error", color=ft.colors.RED_300),
                        content=ft.Text(f"Ocurrió un error: {e}", color=ft.colors.RED_300),
                        actions=[ft.TextButton(text="Aceptar", on_click=lambda e: page.close(error_alert))],
                        bgcolor=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(10)
                    )
                    page.open(error_alert)
                    page.update()
    
    #filtro para validaciones
    def filtro_valid_login(page, data_values, data_keys, errores):
            # Validaciones
            for i in range(len(data_values)):
                value = data_values[i]
                key = data_keys[i]
                      
                if key == "username":
                    error = validate_login(page, value, col_valid_username, txt_valid_username, username_field, icon_valid_username)
                elif key == "password":
                    error = validate_login(page, value, col_valid_password, txt_valid_password, password_field, icon_valid_password)
               
                else:
                    error = None

                if error:
                    errores.append(f"Error en {key}: {error}")

    #----------------------------------------------------------------------------------------------------------------------------------------------
        
    #ÍCONO PARA VALIDACIONES
       
    icon_valid_username=ft.Icon()
    icon_valid_password=ft.Icon()

    #----------------------------------------------------------------------------------------------------------------------------------------------

    # Elementos de la vista de inicio de sesión

    username_field=ft.TextField(
            label="Nombre de Usuario",
            prefix_icon=ft.icons.PERSON,
            hint_text="Nombre de Usuario",
            autofocus=True,
            content_padding=0,
            color=color,
            #text_size=14,
            hint_style=ft.TextStyle(
                #color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                weight="normal"
                ),
            label_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            focused_color=color_primary,
            focused_border_color=color_primary,
            focused_border_width=1,
            border_color=color_hint,
            border_radius=10,
        )
    #texto para validacion de campo username_field
    txt_valid_username=ft.Text()

    password_field=ft.TextField(
            label="Contraseña",
            prefix_icon=ft.icons.LOCK,
            hint_text="Contraseña",
            content_padding=0,
            color=color,
            #text_size=14,
            hint_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                weight="normal"
                ),
            label_style=ft.TextStyle(
                color=color_hint,  # Color del texto de sugerencia
                size=14,  # Tamaño de la fuente del texto de sugerencia
                ),
            fill_color=ft.colors.WHITE,
            focused_color=color_primary,
            focused_border_color=color_primary,
            focused_border_width=1,
            border_color=color_hint,
            border_radius=10,
            password=True,
            can_reveal_password=True,
        )
    #texto para validacion de campo password_field
    txt_valid_password=ft.Text()

    chbx_terminos=ft.Checkbox(
        active_color=color_primary,
        fill_color={
        ft.ControlState.HOVERED: color_hovered,
        ft.ControlState.FOCUSED: color_primary,
        },
        check_color=ft.colors.WHITE
        )
    
    login_button = ft.FilledButton(
        text="Iniciar Sesión", 
        width=300,
        height=40,
        on_click=handle_login,
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
    ))

    back_button = ft.TextButton(
        text="Registrarse",
        width=300,
        on_click=ir_register, # Ajuste para registro
        style=ft.ButtonStyle(
            shape=ft.StadiumBorder(),
            color={
                ft.ControlState.HOVERED: color_primary,
                ft.ControlState.FOCUSED: color_primary,
                ft.ControlState.DEFAULT: color,
            },
            bgcolor={
                ft.ControlState.HOVERED: color_secondary,
                ft.ControlState.DEFAULT: color_secondary,
            },
            #side={
            #        ft.ControlState.DEFAULT: ft.BorderSide(1, "#333333"),
            #        ft.ControlState.HOVERED: ft.BorderSide(2, "#0165BD"),
            #    },
        )
    )

    #Contenedores para columnas
    col_username=ft.Container(content=ft.Column([
                username_field
            ],horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ), width=300,
            #border=ft.border.all()
            )
    col_valid_username=ft.Container(content=ft.Row([
                icon_valid_username,
                txt_valid_username    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
    
    col_password=ft.Container(content=ft.Column([
                password_field
            ],horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ), width=300,
            #border=ft.border.all()
            )
    col_valid_password=ft.Container(content=ft.Row([
                icon_valid_password,
                txt_valid_password    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5, 
            #border=ft.border.all()
            )
    row_username=ft.Container(content=ft.Column([
                col_username,
                col_valid_username
        ], spacing=0
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )
    row_password=ft.Container(content=ft.Column([
                col_password,
                col_valid_password
        ], spacing=0
        ),
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

    # Containers con elementos

    titulo_principal = ft.Container(
        content=ft.Text(
            spans=[
                ft.TextSpan(
                    "Inicia sesión con tu cuenta de usuario.",
                    ft.TextStyle(
                        font_family="RoundsNeue-1",
                        size=15,
                        height=1.5,
                        color=color_primary
                    ))
            ],text_align="center"
        ),margin=ft.margin.only(bottom=10), width=300
        # margin=ft.margin.only(bottom=10)  # Margen inferior para separar del formulario
    )
    imagen= ft.Image(src=f"/logo-neuroiaacv.png", width=200,height=50, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.FIT_HEIGHT)

    row_imagen = ft.Container(
        content=ft.Column(controls=[imagen], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=300, height=50, margin=ft.margin.only(top=30, bottom=20),
    )

    terminos_privacidad = ft.Container(
        content=ft.Row(controls=[chbx_terminos, ft.Text("Acepto los términos y condiciones.",color=color)],spacing=0),
        width=300,
    )
    
    botones = ft.Container(
        content=ft.Column(controls=[ login_button, back_button], alignment=ft.MainAxisAlignment.CENTER),
        width=300, margin=ft.margin.only(top=10)
    )

    contenedor_fondo=ft.Container(width=2000, height=300, bgcolor=color_primary)

    # Container principal de la vista de inicio de sesión
    contenedor_principal = ft.Container(
        content=ft.Column(
            controls=[row_imagen, titulo_principal, row_username, row_password, terminos_privacidad, botones],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        width=400,
        margin=ft.margin.only(top=110, left=20, right=20, bottom=10),
        padding=ft.padding.only( left=20, right=20, bottom=20),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.5, ft.colors.GREY),
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
    )


    contenedor_stack=ft.Stack(controls=[
        contenedor_fondo,
        contenedor_principal
    ],)

    content_scrollable = ft.ListView(
        controls=[contenedor_stack],
        expand=True,
    )

    page.add(content_scrollable)
    page.update()
