from datetime import datetime
import flet as ft
import requests
import threading
import re
from validation import validate_texto, validate_password, validate_email, validate_celular, validate_radiobutton, validate_fecha_nacimiento

global paciente_data, user_data

def registration_view(page, app_state):
    API_URL = 'http://localhost:8080/paciente/register/'

    def back(e):
        page.controls.clear()
        app_state.show_login()
        page.update()
    
    #filtro para validaciones
    def filtro_validaciones(page, data_values, data_keys, errores):
        # Validaciones
        for i in range(len(data_values)):
            value = data_values[i]
            key = data_keys[i]
            
            if key == "nombres":
                error = validate_texto(page, value, 100,col_valid_nombres,txt_valid_nombres,nombres_field,icon_valid_nombres)
            elif key == "apPaterno":
                error = validate_texto(page, value, 100,col_valid_apPaterno,txt_valid_apPaterno,apPaterno_field,icon_valid_apPaterno)
            elif key == "apMaterno":
                error = validate_texto(page, value, 100,col_valid_apMaterno,txt_valid_apMaterno,apMaterno_field,icon_valid_apMaterno)
            elif key == "genero":
                error = validate_radiobutton(page, value, col_valid_genero, txt_valid_genero, col_genero, icon_valid_genero)
            elif key == "fecha_nacimiento":
                error = validate_fecha_nacimiento(page, value, col_valid_fecha, txt_valid_fecha, fecha_nacimiento_field, icon_valid_fecha)
            elif key == "email":
                error = validate_email(page, value, 100, col_valid_email,txt_valid_email,email_field,icon_valid_email)
            elif key == "celular":
                error = validate_celular(page, value, col_valid_celular,txt_valid_celular,celular_field,icon_valid_celular)
            elif key == "username":
                error = validate_texto(page, value, 100,col_valid_username,txt_valid_username,username_field,icon_valid_username)
            elif key == "password":
                error = validate_password(page, value, 100,col_valid_password,txt_valid_password,password_field,icon_valid_password)
            else:
                error = None

            if error:
                errores.append(f"Error en {key}: {error}")
    
    def handle_registration(e):
        user = {
            "username": username_field.value,
            "password": password_field.value
        }

        data = {
            "user": user,
            "nombres": nombres_field.value,
            "apPaterno": apPaterno_field.value,
            "apMaterno": apMaterno_field.value,
            "genero": genero_field.value,  # Valor seleccionado en RadioGroup
            "fecha_nacimiento": fecha_nacimiento_field.value,
            "email": email_field.value,
            "celular": celular_field.value,
        }

        data_values = [value for key, value in data.items() if key != "user"]+list(user.values())
        data_keys = [key for key in data.keys() if key != "user"]+list(user.keys())

        # Lista para errores
        errores = []
        #Llamada al método para validaciones
        filtro_validaciones(page, data_values, data_keys, errores)

        # Imprimir errores

        list_errores="\n".join(errores)

        if errores:
            error_alert = ft.AlertDialog(
                title=ft.Text("Error", color=ft.colors.RED),
                content=ft.Text(list_errores, color=ft.colors.RED),
                bgcolor=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(10)
            )
            page.open(error_alert)

        else:
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
                    print(data)
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

    #----------------------------------------------------------------------------------------------------------------------------------------------    
    #ÍCONO PARA VALIDACIONES
    icon_valid_username=ft.Icon()            
    icon_valid_password=ft.Icon()
    icon_valid_nombres=ft.Icon()
    icon_valid_apPaterno=ft.Icon()
    icon_valid_apMaterno=ft.Icon()
    icon_valid_email=ft.Icon()
    icon_valid_celular=ft.Icon()
    icon_valid_genero=ft.Icon()
    icon_valid_fecha=ft.Icon()
    #----------------------------------------------------------------------------------------------------------------------------------------------
        
    #borde de textfields:
    border_textfield="#777777"

    # Elementos del formulario de registro
    username_field = ft.TextField(label="Nombre de Usuario", prefix_icon=ft.icons.PERSON, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300,border_color=border_textfield,
                        )
    app_state.username_fiel=username_field
    password_field = ft.TextField(label="Contraseña", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300,border_color=border_textfield,
                        )
    nombres_field = ft.TextField(label="Nombres", prefix_icon=ft.icons.PERSON, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300, border_color=border_textfield, capitalization=ft.TextCapitalization.WORDS,
                        )
    apPaterno_field = ft.TextField(label="Apellido Paterno", prefix_icon=ft.icons.PERSON, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300, border_color=border_textfield, capitalization=ft.TextCapitalization.WORDS,
                        )
    apMaterno_field = ft.TextField(label="Apellido Materno", prefix_icon=ft.icons.PERSON, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300,border_color=border_textfield, capitalization=ft.TextCapitalization.WORDS,
                        )
    email_field = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300, border_color=border_textfield,
                        )
    celular_field = ft.TextField(label="Celular", prefix_icon=ft.icons.PHONE, width=300, content_padding=5, color="#333333",
                        #fill_color=ft.colors.WHITE,
                        focused_border_color=ft.colors.BLUE_300, border_color=border_textfield
                        )

    # Radio buttons for gender
    generoLabel = ft.Row(
        [
            ft.Icon(name=ft.icons.MALE, color="#333333"),
            ft.Text("Género", color="#333333", size=17),
        ])
    genero_field = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(
                value="Femenino", 
                label="Femenino",
                label_style=ft.TextStyle(
                    color="#333333",
                    size=14,)),
            ft.Radio(
                value="Masculino", 
                label="Masculino",
                label_style=ft.TextStyle(
                    color="#333333",
                    size=14,)),
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        spacing=0))
    col_genero=ft.Container(content=ft.Column([
                generoLabel,
                genero_field,
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color=border_textfield),
            border_radius=5)
    fecha_nacimiento_field = ft.TextField(
        label="Nacimiento",
        width=180,  # Ajusta el ancho del campo de texto según sea necesario
        read_only=True,
        content_padding=5, color="#333333",
        #fill_color=ft.colors.WHITE,
        focused_border_color=ft.colors.BLUE_300,
        border_color=border_textfield)
    fecha_nacimiento_button = ft.FilledButton(
        "Fecha",
        icon=ft.icons.CALENDAR_MONTH,
        icon_color="#dddddd",  # Cambia el color del ícono
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=1920, month=1, day=1),
                last_date=datetime(year=2024, month=12, day=31),
                on_change=handle_change,
                on_dismiss=handle_dismissal)),
        width=110,
        style=ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: "#dddddd", 
                ft.ControlState.HOVERED: "#dddddd",  
            },
            bgcolor={
                ft.ControlState.DEFAULT: "#777777",  # Color de fondo por defecto
                ft.ControlState.HOVERED: "#999999",  # Color de fondo al pasar el ratón
            },))
    fecha_nacimiento_row = ft.Row(
        controls=[fecha_nacimiento_button,fecha_nacimiento_field],
        alignment=ft.MainAxisAlignment.CENTER,  # Alineación horizontal
        vertical_alignment=ft.CrossAxisAlignment.CENTER)# Alineación vertical
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
            },))
    back_button = ft.TextButton(
        text="Regresar",
        width=300,
        on_click=back,
        style=ft.ButtonStyle(
            shape=ft.StadiumBorder(),
            color={
                ft.ControlState.HOVERED: "#0165BD",
                ft.ControlState.FOCUSED: "#0165BD",
                ft.ControlState.DEFAULT: "#333333",
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.colors.TRANSPARENT,
                ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
            },
            side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, "#333333"),
                    ft.ControlState.HOVERED: ft.BorderSide(2, "#0165BD"),
            },))
    #textos para validacion de campos----------------------------------------------------------------------------------------------------------
    txt_valid_username=ft.Text()
    txt_valid_password=ft.Text()
    txt_valid_nombres=ft.Text()
    txt_valid_apPaterno=ft.Text()
    txt_valid_apMaterno=ft.Text()
    txt_valid_email=ft.Text()
    txt_valid_celular=ft.Text()
    txt_valid_genero=ft.Text()
    txt_valid_fecha=ft.Text()
    #----------------------------------------------------------------------------------------------------------------------------------------------#
    #CONTAINERS PARA TEXTOS DE VALIDACIÓN
    
    col_valid_username=ft.Container(content=ft.Row([
                icon_valid_username,
                txt_valid_username   
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,) 
    col_valid_password=ft.Container(content=ft.Row([
                icon_valid_password,
                txt_valid_password    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,) 
    col_valid_nombres=ft.Container(content=ft.Row([
                icon_valid_nombres,
                txt_valid_nombres    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)
    col_valid_apPaterno=ft.Container(content=ft.Row([
                icon_valid_apPaterno,
                txt_valid_apPaterno    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)
    col_valid_apMaterno=ft.Container(content=ft.Row([
                icon_valid_apMaterno,
                txt_valid_apMaterno    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)
    col_valid_email=ft.Container(content=ft.Row([
                icon_valid_email,
                txt_valid_email    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)
    col_valid_celular=ft.Container(content=ft.Row([
                icon_valid_celular,
                txt_valid_celular    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)
    col_valid_genero=ft.Container(content=ft.Row([
                icon_valid_genero,
                txt_valid_genero    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)   
    col_valid_fecha=ft.Container(content=ft.Row([
                icon_valid_fecha,
                txt_valid_fecha    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)
    #------------------------------------------------------------------------------------------------------------------------------------------------
    #CONTAINERS PARA FILAS DE CAMPOS DE FORMULARIO

    row_username=ft.Container(content=ft.Column([       
                username_field,
                col_valid_username

        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_password=ft.Container(content=ft.Column([       
                password_field,
                col_valid_password

        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_nombres=ft.Container(content=ft.Column([       
                nombres_field,
                col_valid_nombres

        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_apPaterno=ft.Container(content=ft.Column([       
                apPaterno_field,
                col_valid_apPaterno
        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_apMaterno=ft.Container(content=ft.Column([       
                apMaterno_field,
                col_valid_apMaterno
        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_email=ft.Container(content=ft.Column([       
                email_field,
                col_valid_email
        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_celular=ft.Container(content=ft.Column([       
                celular_field,
                col_valid_celular
        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_genero=ft.Container(content=ft.Column([       
                col_genero,
                col_valid_genero
        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)
    row_fecha=ft.Container(content=ft.Column([       
                fecha_nacimiento_row,
                col_valid_fecha
        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center)    

    # Containers con elementos
    separador = ft.Container(width=300, height=20)
    titulo_principal = ft.Container(
        content=ft.Text(
            spans=[
                ft.TextSpan(
                    "Formulario de Registro",
                    ft.TextStyle(size=20, color='#333333')),
            ],),
        margin=ft.margin.only(bottom=20)  # Margen inferior para separar del formulario
    )
    campos_formulario = ft.Container(
        content=ft.Column(controls=[
            row_nombres, 
            row_apPaterno,
            row_apMaterno,
            row_genero, 
            row_fecha,
            row_email,
            row_celular,
            row_username,
            row_password,
        ], alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=300)
    
    botones = ft.Container(
        content=ft.Column(controls=[register_button, back_button], alignment=ft.MainAxisAlignment.CENTER),
        width=300, margin=ft.margin.only(top=20))

    # Container principal de la vista de registro
    contenedor_principal = ft.Container(
        content=ft.Column(
            controls=[separador, 
                      titulo_principal, 
                      campos_formulario, 
                      botones],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        width=400)

    content_scrollable = ft.ListView(
        controls=[contenedor_principal],
        expand=True,)

    page.add(content_scrollable)
    page.update()
