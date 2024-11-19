import flet as ft
from flet import *
from login import login_view
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_boton, color_titulo
from menubar import menubar

#VISTA PRINCIPAL
def welcome_view (page, app_state):

    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
        page.controls.clear()
        login_view(page, app_state)
        page.update()
        return

    username = app_state.user_data.get('username', 'Usuario')


    def ir_home(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_home()
        page.update()

    #ELEMENTOS DE VISTA PRINCIPAL

    t_p=ft.Text(
        spans=[
                ft.TextSpan(
                    f"Bienvenido {username} a ",
                    ft.TextStyle(size=30, color=color, height=1 )),
                ft.TextSpan(
                    "CHIKITINES S.A.C ",
                    ft.TextStyle(
                        font_family="RoundsNeue-4",
                        size=30,
                        height=1,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [color_titulo, ft.colors.LIGHT_BLUE]
                            )
                        ),
                    ),),
                        
        ])
    t_s = ft.Text(value='"App para la prediccion de la demanda"',size=18, color=color, font_family="RoundsNeue-1", text_align="center")
    i_p= ft.Image(src=f"/logo_pequeño.jpg", width=300, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.FIT_HEIGHT)
    b_p = ft.FilledButton(
        text="Continuar",
        width=300, 
        height=40,  
        on_click=lambda e: ir_home(e, page, app_state),
        style=ft.ButtonStyle(
            shape=ft.StadiumBorder(),
            color={
                ft.ControlState.HOVERED: ft.colors.WHITE,
                ft.ControlState.FOCUSED: ft.colors.WHITE,
                ft.ControlState.DEFAULT: ft.colors.WHITE,
            },
            bgcolor={
                ft.ControlState.HOVERED: color_hovered,
                ft.ControlState.DEFAULT: color_boton,
            }
        )
        )
    
    
    #CONTAINERS CON ELEMENTOS
    separador = ft.Container(
        width=300,
        height=20,
        #border=ft.border.all()
    )
    titulo_principal = ft.Container(
        content=ft.Column(controls=[t_p
        ]),width=300)
    titulo_secundario = ft.Container(
        content=ft.Column(controls=[t_s
        ]),width=300)
    imagen_principal = ft.Container(
        content=ft.Column(controls=[i_p
        ]),width=300,margin=ft.margin.only(top=10))
    boton_principal = ft.Container(content=ft.Column(controls =[b_p],
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
        ), width=300,margin=ft.margin.only(top=10))
  
    #CONTAINER PRINCIPAL DE VISTA PRINCIPAL
    contenedor_principal= ft.Container( content=ft.Column([
            separador,
            titulo_principal,
            titulo_secundario,
            imagen_principal,
            boton_principal,
        ], 
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
        ),
        expand=True,
        width=400
        )
   
    content_principal_scrollable = ft.ListView(
        controls=[contenedor_principal,],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
    )


    page.add(content_principal_scrollable)
    page.update()


