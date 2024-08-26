import flet as ft
from flet import *
import requests
from login import login_view
from datetime import datetime
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered, desplegable_diagnostico
from menubar import menubar
from urlsapi import HTTP_UPDATE_PACIENTE

def view_setting(page, app_state):

    page.padding=0

    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return
            
    #Obtener token
    token =app_state.token

    
    #consumir API aquí!


    def ir_home(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_home()
        page.update()

    #----------------------------------------------------------------------------------------------------------------------------------------------    
    #ÍCONO PARA VALIDACIONES
    icon_valid_username=ft.Icon()            
    icon_valid_nombres=ft.Icon()
    icon_valid_apPaterno=ft.Icon()
    icon_valid_apMaterno=ft.Icon()
    icon_valid_email=ft.Icon()
    icon_valid_celular=ft.Icon()
    icon_valid_genero=ft.Icon()
    icon_valid_fecha=ft.Icon()

    
    #variables de usuario y paciente:

    user = app_state.user_data.get('username', 'Usuario')
    nombres = app_state.paciente_data.get('nombres', 'Nombres')
    apPaterno = app_state.paciente_data.get('apPaterno', 'Apellido Paterno')
    apMaterno = app_state.paciente_data.get('apMaterno', 'Apellido Materno')
    email = app_state.paciente_data.get('email', 'Email')
    celular = app_state.paciente_data.get('celular', 'Celular')
    genero = app_state.paciente_data.get('genero', 'Género')
    fecha_nacimiento = app_state.paciente_data.get('fecha_nacimiento', 'Fecha de nacimiento')

    """ username_field.value
    nombres_field
    apPaterno_field
    apMaterno_field
    email_field
    celular_field
    genero_field
    fecha_nacimiento_field """
    #----------------------------------------------------------------------------------------------------------------------------------------------
     
    # Elementos del formulario de registro
    username_field = ft.TextField(label="Nombre de Usuario", prefix_icon=ft.icons.PERSON, width=300, 
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
            value=user,
                        )

    
    nombres_field = ft.TextField(label="Nombres", prefix_icon=ft.icons.PERSON, width=300, autofocus=True,
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
            capitalization=ft.TextCapitalization.WORDS,
            value=nombres,
                        )
    
    apPaterno_field = ft.TextField(label="Apellido Paterno", prefix_icon=ft.icons.PERSON, width=300, autofocus=True,
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
            capitalization=ft.TextCapitalization.WORDS,
            value=apPaterno,
                        )

    apMaterno_field = ft.TextField(label="Apellido Materno", prefix_icon=ft.icons.PERSON, width=300, 
            value=apMaterno,
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
            capitalization=ft.TextCapitalization.WORDS,
                        )

    email_field = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, width=300, 
            value=email,
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

    celular_field = ft.TextField(label="Celular", prefix_icon=ft.icons.PHONE, width=300,
            value=celular, 
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
        spacing=0), value=genero)
    col_genero=ft.Container(content=ft.Column([
                generoLabel,
                genero_field,
            ]
            ), width=300,
            #margin=ft.margin.only(left=10, top=10, right=10),
            padding=15,
            border=ft.border.all(color=color_hint),
            border_radius=10)

    fecha_nacimiento_field = ft.TextField(
        label="Nacimiento",
        width=150,  # Ajusta el ancho del campo de texto según sea necesario
        read_only=True,
        autofocus=True,
            content_padding=ft.padding.only(left=10),
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
            value=fecha_nacimiento)
    
    def handle_change(e):
        fecha_nacimiento_field.value = e.control.value.strftime('%Y-%m-%d')
        page.update()


    fecha_nacimiento_button = ft.FilledButton(
        "Fecha",
        icon=ft.icons.CALENDAR_MONTH,
        icon_color=color_primary,  # Cambia el color del ícono
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=1920, month=1, day=1),
                last_date=datetime(year=2024, month=12, day=31),
                on_change=handle_change,)),
        width=110,
        style=ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: color_primary, 
                ft.ControlState.HOVERED: color_primary,  
            },
            bgcolor={
                ft.ControlState.HOVERED: color_secondary,
                ft.ControlState.DEFAULT: color_secondary,
            },))


    fecha_nacimiento_row = ft.Container(content=ft.Row(
        [fecha_nacimiento_button,fecha_nacimiento_field],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Alineación horizontal
        vertical_alignment=ft.CrossAxisAlignment.CENTER),)# Alineación vertical
    
    update_button = ft.FilledButton(
        text="Actualizar",
        width=300,
        height=40,
        #on_click=actualizar_datos,
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
            },))
    back_button = ft.TextButton(
        text="Regresar",
        width=300,
        on_click=lambda e: ir_home(e, page, app_state),
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
            },))
    #textos para validacion de campos----------------------------------------------------------------------------------------------------------
    txt_valid_username=ft.Text()
    #txt_valid_password=ft.Text()
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
    """ col_valid_password=ft.Container(content=ft.Row([
                icon_valid_password,
                txt_valid_password    
            ]
            ), width=300,
            height=10,
            padding=5,
            border_radius=5,)  """
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
    """ row_password=ft.Container(content=ft.Column([       
                #password_field,
                col_valid_password

        ], spacing=0),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center) """
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

    titulo_principal=ft.Container(content=ft.Column([       
        ft.Text("Actualizar Perfil",size=20, color=ft.colors.WHITE),
        ft.Text("Modifique los campos que desea actualizar.",size=10, color=ft.colors.WHITE)
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        #padding=ft.padding.only(top=10), 
        alignment=ft.alignment.center, margin=ft.margin.only(top=40))


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
            #row_password,
        ], alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=300,
        padding=ft.padding.only(top=30))
    
    botones = ft.Container(
        content=ft.Column(controls=[update_button, back_button], alignment=ft.MainAxisAlignment.CENTER),
        width=300)

    contenedor_fondo=ft.Container(width=2000, height=100, bgcolor=color_primary)

    # Container principal de la vista de registro
    contenedor_principal = ft.Container(
        content=ft.Column(
            controls=[
                      campos_formulario, 
                      botones],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),margin=ft.margin.only(top=20, left=20, right=20, bottom=30),
        padding=ft.padding.only( left=20, right=20, bottom=20),
        expand=True,
        width=400,
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        #shadow=ft.BoxShadow(
        #    spread_radius=1,
        #    blur_radius=15,
        #    color=ft.colors.with_opacity(0.5, ft.colors.GREY),
        #    offset=ft.Offset(0, 0),
        #    blur_style=ft.ShadowBlurStyle.OUTER,
        #)
        )

    contenedor_stack=ft.Stack([
        contenedor_fondo,
        titulo_principal,
    ],)

    content_scrollable = ft.ListView(
        controls=[contenedor_principal],
        expand=True,
    )
    page.add(contenedor_stack)
    page.add(content_scrollable)
    page.update()