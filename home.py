import flet as ft
from navigator import navigator_component
from login import login_view
from styles import color, color_hint, color_primary, color_secondary, color_hovered
from menubar import menubar

#VISTA CON OPCIONES DE PREDICCIÓN
def home_view(page, app_state):

    if not app_state.token:
        page.controls.clear()
        login_view(page, app_state)
        page.update()
        return
    
    def show_form(e, form_id, page, app_state):
            if form_id == "form_1":
                page.controls.clear()
                menu_bar=menubar(page, app_state)
                page.controls.append(menu_bar)
                page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
                app_state.show_objetive1()
            elif form_id == "form_2":
                page.controls.clear()
                menu_bar=menubar(page, app_state)
                page.controls.append(menu_bar)
                page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
                app_state.show_objetive2()
            elif form_id == "form_3":
                page.controls.clear()
                menu_bar=menubar(page, app_state)
                page.controls.append(menu_bar)
                page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
                app_state.show_objetive3()
            else:
                print(f"Formulario con ID {form_id} no encontrado")

    def create_card(objetivo, nombre, form_id, img):

            txt_objetivo = ft.Text(spans=[
                ft.TextSpan(
                    objetivo,
                    ft.TextStyle(
                        font_family="RoundsNeue-2",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=color
                    ),),
                        
            ])
            
            txt_descripcion =  ft.Text(nombre, style=ft.TextStyle(size=12, color='#9c9c9c'))

            btn_formulario = ft.FilledButton(
                    text="Continuar",
                    width=150,
                    height=30,
                    on_click=lambda e: show_form(e, form_id, page, app_state),
                    style=ft.ButtonStyle(
                        shape=ft.StadiumBorder(),
                        color={
                            ft.ControlState.HOVERED: ft.colors.WHITE,
                            ft.ControlState.FOCUSED: ft.colors.WHITE,
                            ft.ControlState.DEFAULT: ft.colors.WHITE,
                        },
                        bgcolor={
                            ft.ControlState.HOVERED: color_hovered,
                            ft.ControlState.DEFAULT:  "#75b376" ,
                        }
                    )
                    )
            
            #ELEMENTOS PARA IZQUIERDA_CONTAINER         
            if img == 1:
                imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/objetivo1.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.CONTAIN)
                ]),width=100)
            elif img == 2:
                imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/objetivo2.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.CONTAIN)
                ]),width=100)
            else:
                imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/objetivo3.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.CONTAIN)
                ]),width=100)

            derecha_container=ft.Container(content=ft.Column([
                    txt_objetivo,
                    txt_descripcion,
                    btn_formulario

            ]), width=170)
            izquierda_container=ft.Container(content=ft.Column([
                    imagen_principal
            ]), width=100)

            return ft.Container(
                content=ft.Row([
                    derecha_container,
                    izquierda_container

                ], spacing=0, alignment="center"), 
                width=300,
                padding=15,
                border_radius=15,
                border=ft.border.all(color=color_hint),
                bgcolor=ft.colors.WHITE,
                margin=ft.margin.only(bottom=10)
                #border=ft.border.all()
            )

    def accion_volver_welcome(e):
            page.controls.clear()
            #page.appbar.visible = not page.appbar.visible
            page.navigation_bar.visible = not page.navigation_bar.visible
            app_state.show_welcome()
            page.update()

    #ELEMENTOS DE VISTA HOME
    #boton en texto -> < VOLVER
    texto_volver = ft.Container(
        content=ft.TextButton(
            on_click=accion_volver_welcome,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.ARROW_BACK_IOS_SHARP, color="#000000", size=11),
                    ft.Container(width=5),
                    ft.Text("Volver", color="#000000")
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
        ),
        alignment=ft.alignment.top_left,  # Alineado a la derecha
        margin=ft.margin.only(right=15, top=2, bottom=1),  # Margen de 20 píxeles a la derecha y 10 píxeles en la parte superior
    )
        

#CONTAINERS CON ELEMENTOS
    option_container_home = ft.Container(
        content=ft.Row(controls=[texto_volver
        ]  # Alinear a la derecha
        ),width=300)
    
    #CONTAINER PRINCIPAL DE HOME
    cards = ft.Container( content=ft.Column([
                option_container_home,
                create_card("PREDICCIÓN DE LA DEMANDA", "Prediccion de la demanda por variables", "form_1", 1),
                create_card("ANÁLISIS POR CLUSTERS", "Visualiza el análisis de clustering de productos", "form_2", 2),
                create_card("MARKET BASKET ANALYSIS", "Algoritmo de minería de datos que identifica conjuntos de ítems frecuentes", "form_3", 3),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
            ))
    
    cards_scrollable = ft.ListView(
        controls=[cards],
        expand=True,  
    )

    navigator_component(page, app_state)
    page.controls.append(cards_scrollable)
    page.update()
        
