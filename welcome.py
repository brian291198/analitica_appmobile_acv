import flet as ft
from flet import *

#VISTA PRINCIPAL
def welcome_view (page, app_state):

    def ir_home(e):
        page.controls.clear()
        app_state.show_home()
        page.update()

    #ELEMENTOS DE VISTA PRINCIPAL

    t_p=ft.Text(
        spans=[
                ft.TextSpan(
                    "La mejor APP para predecir el riesgo de ",
                    ft.TextStyle(size=30, color='#333333')),
                ft.TextSpan(
                    "ACV",
                    ft.TextStyle(size=30,weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600))
                        
        ])
    t_s = ft.Text(value='"Cuida tu futuro hoy"',size=15, color='#333333')
    i_p= ft.Image(src=f"/principal.png", width=300, height=300, repeat=ft.ImageRepeat.NO_REPEAT,)
    b_p = ft.FilledButton(
        text="Continuar",
        width=300, 
        height=40,  
        on_click=ir_home,
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
        ]),width=300)
    boton_principal = ft.Container(content=ft.Column(controls =[b_p],
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
        ), width=300)
  
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
        width=400,
        #border=ft.border.all()
        )
    content_principal_scrollable = ft.ListView(
        controls=[contenedor_principal,],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
    )


    page.add(content_principal_scrollable)
    page.update()


 