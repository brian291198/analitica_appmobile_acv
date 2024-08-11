import flet as ft
from navigator import navigator_component
from login import login_view
from styles import color, color_hint, color_primary, color_secondary, color_hovered
from menubar import menubar

#VISTA CON OPCIONES DE PREDICCIÓN
def home_view(page, app_state):
    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
        page.controls.clear()
        login_view(page, app_state)
        page.update()
        return
    

    def show_form(e, form_id, page, app_state):
            if form_id == "form_1":
                page.controls.clear()
                menu_bar=menubar(page, app_state)
                page.controls.append(menu_bar)
                page.controls.append(ft.Container(height=1, bgcolor=color_hint, width=300))
                app_state.show_objetive1()
            elif form_id == "form_2":
                page.controls.clear()
                menu_bar=menubar(page, app_state)
                page.controls.append(menu_bar)
                page.controls.append(ft.Container(height=1, bgcolor=color_hint, width=300))
                app_state.show_objetive2()
            elif form_id == "form_3":
                page.controls.clear()
                menu_bar=menubar(page, app_state)
                page.controls.append(menu_bar)
                page.controls.append(ft.Container(height=1, bgcolor=color_hint, width=300))
                app_state.show_objetive3()
            else:
                print(f"Formulario con ID {form_id} no encontrado")

    def create_card(objetivo, nombre, form_id, img):

            #ELEMENTOS PARA DERECHA_CONTAINER          
            #txt_objetivo = ft.Text(objetivo, style=ft.TextStyle(size=18, color=ft.colors.BLUE_500, font_family="RoundsNeue-3"))

            """ txt_objetivo = ft.Text(spans=[
                ft.TextSpan(
                    objetivo,
                    ft.TextStyle(
                        font_family="RoundsNeue-3",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [ft.colors.BLUE_700, ft.colors.LIGHT_BLUE_400]
                            )
                        ),
                    ),),
                        
            ]) """
            txt_objetivo = ft.Text(spans=[
                ft.TextSpan(
                    objetivo,
                    ft.TextStyle(
                        font_family="RoundsNeue-2",
                        size=18,
                        #weight=ft.FontWeight.BOLD,
                        color=color
                    ),),
                        
             ])
            
            txt_descripcion =  ft.Text(nombre, style=ft.TextStyle(size=12, color='#333333'))
            btn_formulario = ft.FilledButton(
                    text="Continuar",
                    width=170,
                    height=40,
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
                            ft.ControlState.DEFAULT: color_primary,
                        }
                    )
                    )
            #ELEMENTOS PARA IZQUIERDA_CONTAINER         

            if img == 1:
                imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj1.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.CONTAIN)
                ]),width=100)
            elif img == 2:
                imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj2.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.CONTAIN)
                ]),width=100)
            else:
                imagen_principal = ft.Container(
                    content=ft.Column(controls=[
                        ft.Image(src=f"/obj3.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,fit=ft.ImageFit.CONTAIN)
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
                border_radius=20,
                border=ft.border.all(color=color_hint),
                bgcolor=ft.colors.WHITE,
                margin=ft.margin.only(bottom=20)
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
    texto_volver = ft.TextButton(
        on_click=accion_volver_welcome,
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.ARROW_BACK_IOS_SHARP, color="#333333", size=10),
                ft.Container(width=5),
                ft.Text("Volver", color="#333333")
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
    )
    

#CONTAINERS CON ELEMENTOS
 
    option_container_home = ft.Container(
        content=ft.Row(controls=[texto_volver
        ], alignment=ft.MainAxisAlignment.END  # Alinear a la derecha
        ),width=300, margin=10)
    
    #CONTAINER PRINCIPAL DE HOME
    cards = ft.Container( content=ft.Column([

                option_container_home,
                create_card("Diagnóstico de ACV", "Diagnóstico rápido realizado mediante machine learning", "form_1", 1),
                create_card("Segmentación de pacientes", "Clasificados bajo factores médicos", "form_2", 2),
                create_card("Segmentación de pacientes", "Clasificados bajo estilo de vida", "form_3", 3),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
            ))
    cards_scrollable = ft.ListView(
        controls=[cards],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
    )
    navigator_component(page, app_state)
    page.controls.append(cards_scrollable)
    page.update()
        
