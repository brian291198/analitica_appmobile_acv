import flet as ft
import requests

def login_view(page, app_state):
    API_URL = 'http://localhost:8080/login/'

    def ir_register(e):
        page.controls.clear()
        app_state.show_register()
        page.update()

    def handle_login(e):
        username = username_field.value
        password = password_field.value

        # Validar que los campos no estén vacíos
        if not username.strip() or not password.strip():
            error_alert = ft.AlertDialog(
                title=ft.Text("Error", color=ft.colors.RED),
                content=ft.Text("Por favor, complete todos los campos.", color=ft.colors.RED),
                # actions=[ft.TextButton(text="Aceptar", on_click=lambda e: page.close(error_alert))],
                bgcolor=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(10)
            )
            page.open(error_alert)
            page.update()
            return

        datos = {
            "username": username,
            "password": password
        }
        headers = {'Content-Type': 'application/json'}

        # Mostrar mensaje de carga
        loading_dialog = ft.AlertDialog(
            title=ft.Text("Cargando...", color=ft.colors.BLACK),
            content=ft.Text("Por favor, espere mientras se procesa su solicitud.", color=ft.colors.BLACK),
            actions=[],
            bgcolor=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(10)
        )
        page.open(loading_dialog)
        page.update()

        try:
            response = requests.post(API_URL, json=datos, headers=headers)
            page.close(loading_dialog)
            if response.status_code == 200:
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

                def close_error_dialog(e):
                    page.close(error_alert)
                    page.update()

                error_alert = ft.AlertDialog(
                    title=ft.Text("Error de Inicio de Sesión", color=ft.colors.RED),
                    content=ft.Text(error_message, color=ft.colors.RED),
                    # actions=[ft.TextButton(text="Aceptar", on_click=close_error_dialog)],
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(10)
                )
                page.open(error_alert)
                page.update()

        except Exception as e:
            # Mostrar un mensaje de error en la interfaz
            error_alert = ft.AlertDialog(
                title=ft.Text("Error", color=ft.colors.RED),
                content=ft.Text(f"Ocurrió un error: {e}", color=ft.colors.RED),
                actions=[ft.TextButton(text="Aceptar", on_click=lambda e: page.close(error_alert))],
                bgcolor=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(10)
            )
            page.open(error_alert)
            page.update()

    # Elementos de la vista de inicio de sesión


    username_field =ft.TextField(
            label="Nombre de Usuario",
            prefix_icon=ft.icons.PERSON,
            width=300, 
            color="#333333",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            fill_color=ft.colors.WHITE,
            content_padding=5,
        )
    password_field =ft.TextField(
            label="Contraseña",
            prefix_icon=ft.icons.LOCK,
            password=True,
            width=300, 
            color="#333333",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            fill_color=ft.colors.WHITE,
            content_padding=5,
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
                ft.ControlState.HOVERED: ft.colors.BLUE_300,
                ft.ControlState.DEFAULT: "#0165BD",
            },
        )
    )

    back_button = ft.TextButton(
        text="Registrarse",
        width=300,
        on_click=ir_register, # Ajuste para registro
        style=ft.ButtonStyle(
            shape=ft.StadiumBorder(),
            color={
                ft.ControlState.HOVERED: ft.colors.WHITE,
                ft.ControlState.FOCUSED: ft.colors.WHITE,
                ft.ControlState.DEFAULT: "#333333",
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.colors.BLUE_300,
                ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
            },
            side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                },
        )
    )

    # Containers con elementos
    separador = ft.Container(width=300, height=20)
    titulo_principal = ft.Container(
        content=ft.Text(
            spans=[
                ft.TextSpan(
                    "Iniciar Sesión",
                    ft.TextStyle(
                        font_family="LTSaeada-2",
                        size=30,
                        height=1,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), ["#002387", ft.colors.LIGHT_BLUE]
                            )
                        ),
                    ))
            ],text_align="center"
        ),margin=ft.margin.only(top=10, bottom=20)
        # margin=ft.margin.only(bottom=10)  # Margen inferior para separar del formulario
    )
    imagen= ft.Image(src=f"/logo_redondeado.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.FIT_HEIGHT)

    campos_formulario = ft.Container(
        content=ft.Column(controls=[username_field, password_field], alignment=ft.MainAxisAlignment.CENTER),
        width=300
    )
    
    botones = ft.Container(
        content=ft.Column(controls=[login_button, back_button], alignment=ft.MainAxisAlignment.CENTER),
        width=300, margin=ft.margin.only(top=20)
    )

    # Container principal de la vista de inicio de sesión
    contenedor_principal = ft.Container(
        content=ft.Column(
            controls=[separador, imagen, titulo_principal, campos_formulario, botones],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        width=400,
        margin=ft.margin.only(top=20)
    )

    content_scrollable = ft.ListView(
        controls=[contenedor_principal],
        expand=True,
    )

    page.add(content_scrollable)
    page.update()

