import datetime
import flet as ft
import requests
import threading

def registration_view(page, app_state):
    API_URL = 'http://localhost:8080/paciente/register/'

    def back(e):
        page.controls.clear()
        app_state.show_login()
        page.update()

    def handle_registration(e):
        user = {
            "username": username_field.value,
            "password": password_field.value
        }

        data = {
            "user": user,
            "password": password_field.value,
            "nombres": nombres_field.value,
            "apPaterno": apPaterno_field.value,
            "apMaterno": apMaterno_field.value,
            "email": email_field.value,
            "celular": celular_field.value,
            "genero": genero_field.value,  # Valor seleccionado en RadioGroup
            "fecha_nacimiento": fecha_nacimiento_field.value
        }

        def is_empty(value):
            return not (value or "").strip()

        if any(is_empty(value) for value in data.values() if isinstance(value, str)) or not genero_field.value:
            error_alert = ft.AlertDialog(
                title=ft.Text("Error", color=ft.colors.RED),
                content=ft.Text("Por favor, complete todos los campos.", color=ft.colors.RED),
                bgcolor=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(10)
            )
            page.show_dialog(error_alert)
            return

        headers = {'Content-Type': 'application/json'}

        loading_dialog = ft.AlertDialog(
            title=ft.Text("Cargando...", color=ft.colors.BLACK),
            content=ft.Text("Por favor, espere mientras se procesa su solicitud.", color=ft.colors.BLACK),
            actions=[],
            bgcolor=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(10)
        )
        page.show_dialog(loading_dialog)

        try:
            response = requests.post(API_URL, json=data, headers=headers)

            if response.status_code == 201:  # Código de estado HTTP para creación exitosa
                response_data = response.json()
                token = response_data.get('token')
                user_data = response_data.get('user')
                paciente_data = response_data.get('paciente')  

                app_state.token = token
                app_state.user_data = user_data
                app_state.paciente_data = paciente_data  

                page.update()

                success_message = response_data.get("message", "Registro exitoso. Redirigiendo...")

                def redirect_after_delay():
                    page.controls.clear()
                    app_state.show_welcome()
                    page.update()

                success_alert = ft.AlertDialog(
                    title=ft.Text("Éxito", color=ft.colors.GREEN),
                    content=ft.Text(success_message, color=ft.colors.GREEN),
                    actions=[],
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(10)
                )
                page.show_dialog(success_alert)

                threading.Timer(2.0, redirect_after_delay).start() 

            else:
                error_message = response.json().get('message', 'Error desconocido')

                def close_error_dialog(e):
                    page.update()

                error_alert = ft.AlertDialog(
                    title=ft.Text("Error de Registro", color=ft.colors.RED),
                    content=ft.Text(error_message, color=ft.colors.RED),
                    # actions=[ft.TextButton(text="Aceptar", on_click=close_error_dialog)],
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(10)
                )
                page.show_dialog(error_alert)

        except Exception as e:
            error_alert = ft.AlertDialog(
                title=ft.Text("Error", color=ft.colors.RED),
                content=ft.Text(f"Ocurrió un error: {e}", color=ft.colors.RED),
                # actions=[ft.TextButton(text="Aceptar")],
                bgcolor=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(10)
            )
            page.show_dialog(error_alert)

    def handle_change(e):
        fecha_nacimiento_field.value = e.control.value.strftime('%Y-%m-%d')
        page.update()

    def handle_dismissal(e):
        pass

    def on_gender_change(e):
        genero_field.value = e.control.value

    # Elementos del formulario de registro
    username_field = ft.TextField(label="Nombre de Usuario", prefix_icon=ft.icons.PERSON, width=300)
    password_field = ft.TextField(label="Contraseña", prefix_icon=ft.icons.LOCK, password=True, width=300)
    nombres_field = ft.TextField(label="Nombres", prefix_icon=ft.icons.PERSON, width=300)
    apPaterno_field = ft.TextField(label="Apellido Paterno", prefix_icon=ft.icons.PERSON, width=300)
    apMaterno_field = ft.TextField(label="Apellido Materno", prefix_icon=ft.icons.PERSON, width=300)
    email_field = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, width=300)
    celular_field = ft.TextField(label="Celular", prefix_icon=ft.icons.PHONE, width=300)

    # Radio buttons for gender
    generoLabel = ft.Row(
        [
            ft.Icon(name=ft.icons.MALE, color="#333333"),
            ft.Text("Género", color="#333333", size=17),
        ]
    )
    genero_field = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(
                value="Femenino", 
                label="Femenino",
                label_style=ft.TextStyle(
                    color="#333333",
                    size=14,
                )
            ),
            ft.Radio(
                value="Masculino", 
                label="Masculino",
                label_style=ft.TextStyle(
                    color="#333333",
                    size=14,
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        spacing=0),
        on_change=on_gender_change
    )

    colgenero = ft.Container(
        content=ft.Column([
            generoLabel,
            genero_field,
        ]),
        width=300,
        padding=15,
        border=ft.border.all(color="#000000"),
        border_radius=5
    )

    fecha_nacimiento_field = ft.TextField(
        label="Nacimiento",
        width=180,  # Ajusta el ancho del campo de texto según sea necesario
        read_only=True
    )

    fecha_nacimiento_button = ft.ElevatedButton(
        "Fecha",
        icon=ft.icons.CALENDAR_MONTH,
        icon_color=ft.colors.BLACK54,  # Cambia el color del ícono
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=1920, month=1, day=1),
                last_date=datetime.datetime(year=2024, month=12, day=31),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        ),
        width=110,
        style=ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: "#333333", 
                ft.ControlState.HOVERED: "#555555", 
                ft.ControlState.FOCUSED: "#777777", 
            },
        )
    )

    fecha_nacimiento_row = ft.Row(
        controls=[fecha_nacimiento_button,fecha_nacimiento_field],
        alignment=ft.MainAxisAlignment.CENTER,  # Alineación horizontal
        vertical_alignment=ft.CrossAxisAlignment.CENTER  # Alineación vertical
    )

    register_button = ft.FilledButton(
        text="Registrar",
        width=300,
        height=40,
        on_click=handle_registration,
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

    back_button = ft.TextButton(
        text="Regresar",
        width=300,
        on_click=back,
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

    # Containers con elementos
    separador = ft.Container(width=300, height=20)
    titulo_principal = ft.Container(
        content=ft.Text(
            spans=[
                ft.TextSpan(
                    "Formulario de ",
                    ft.TextStyle(size=30, color='#333333')),
                ft.TextSpan(
                    "Registro",
                    ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600))
            ],
        ),
        margin=ft.margin.only(bottom=20)  # Margen inferior para separar del formulario
    )

    campos_formulario = ft.Container(
        content=ft.Column(controls=[
            nombres_field, apPaterno_field,
            apMaterno_field, colgenero, fecha_nacimiento_row, email_field, celular_field, username_field, password_field
        ], alignment=ft.MainAxisAlignment.CENTER),
        width=300
    )
    
    botones = ft.Container(
        content=ft.Column(controls=[register_button, back_button], alignment=ft.MainAxisAlignment.CENTER),
        width=300, margin=ft.margin.only(top=20)
    )

    # Container principal de la vista de registro
    contenedor_principal = ft.Container(
        content=ft.Column(
            controls=[separador, titulo_principal, campos_formulario, botones],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        width=400
    )

    content_scrollable = ft.ListView(
        controls=[contenedor_principal],
        expand=True,
    )

    page.add(content_scrollable)
    page.update()
