import flet as ft
import requests
from login import login_view
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_check, color_error, desplegable_diagnostico
import time

def main_style():
    return {
        "width": 290,
        "height": 420,
        "bgcolor": "white",
    }

def prompt_style():
    return {
        "hint_text": "Escribe algo...",
        "autofocus": True,
        "content_padding": 0,
        "color": "#333333",
        "text_size": 14,
        "hint_style": ft.TextStyle(
            color="#cccccc",  # Color del texto de sugerencia
            size=14,  # Tamaño de la fuente del texto de sugerencia
            weight="normal"
        ),
        "label_style": ft.TextStyle(
            color="#cccccc",  # Color del texto de sugerencia
            size=14,  # Tamaño de la fuente del texto de sugerencia
        ),
        "selection_color": "#333333",
        "cursor_color": "#333333",
        "fill_color": ft.colors.WHITE,
        "focused_border_color": ft.colors.TRANSPARENT,  # Hacer el borde enfocado transparente
        "border_color": ft.colors.TRANSPARENT,
        "width": 200,
        "height": 20,
    }

class MainContentArea(ft.Container):
    def __init__(self) -> None:
        super().__init__(**main_style())
        self.chat = ft.ListView(
            expand=True,
            height=250,
            spacing=0,
            auto_scroll=True,
        )
        self.content = self.chat

class CreateMessageTEXT(ft.Column):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        self.text = ft.Container(
            content=ft.Text(
                self.message,
                color="#333333"
            ),
            bgcolor=desplegable_diagnostico,  # Color de fondo gris
            padding=10,  # Padding de 10
            margin=5,  # Margen de 5
            border_radius=10,  # Bordes redondeados
            #width=300,  # Ancho del contenedor
            #alignment=ft.Alignment.center_left,  # Alineación del texto
            )
        super().__init__(spacing=4)
        #self.controls = [ft.Text(self.name, color="#333333", opacity=0.4), self.text]


        self.controls=[
                ft.Row(
                        [
                            ft.CircleAvatar(
                                content=ft.Text(self.name, size=12),
                                color=ft.colors.WHITE,
                                bgcolor=color_primary,
                            ),
                            ft.Column(
                                [
                                    #ft.Text(message.user_name, weight="bold"),
                                    #ft.Text(message.text, selectable=True),
                                    self.text
                                ],
                                tight=True,
                                spacing=5,
                                width=230
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,  # Alinea el contenido al inicio del Row
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,  # Espaciado entre el avatar y el texto
    
                    )
            ]
class CreateMessageGPT(ft.Column):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        self.text = ft.Container(
            content=ft.Text(
                self.message,
                color="#333333"
            ),
            bgcolor=color_hint,  # Color de fondo gris
            padding=10,  # Padding de 10
            margin=5,  # Margen de 5
            border_radius=10,  # Bordes redondeados
            )
        super().__init__(spacing=4)


        self.controls=[
                ft.Row(
                        [
                            ft.Column(
                                [
                                    self.text
                                ],
                                tight=True,
                                spacing=5,
                                width=230
                            ),
                            ft.CircleAvatar(
                                content=ft.Text(self.name, size=12),
                                color=ft.colors.WHITE,
                                bgcolor=color,
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,  # Alinea el contenido al inicio del Row
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,  # Espaciado entre el avatar y el texto
              
                    )
            ]

class Prompt(ft.TextField):
    def __init__(self, chat: ft.ListView):
        super().__init__(**prompt_style(), on_submit=self.run_prompt)
        self.chat = chat
        #self.text_value = ""  # Variable para almacenar el valor del TextField
    
    def animate_text_output(self, name:str, prompt:str):
        word_list: list = []
        msg = CreateMessageTEXT(name, "")

        #list(prompt) => we deconstruct the prompt text into sepreate characters, and loop over them
        for word in list(prompt):
            word_list.append(word)
            msg.text.value = "".join(word_list)
            self.chat.update()
            #time.sleep(0.008)
    def animate_gpt_output(self, name:str, prompt:str):
        word_list: list = []
        msg = CreateMessageGPT(name, "")

        #list(prompt) => we deconstruct the prompt text into sepreate characters, and loop over them
        for word in list(prompt):
            word_list.append(word)
            msg.text.value = "".join(word_list)
            self.chat.update()
            #time.sleep(0.008)

    """  def user_output(self, prompt):
        msg = CreateMessage("Yo:", prompt)
        self.chat.controls.append(msg)
        self.chat.update() """
    def user_output(self, prompt):
        self.animate_text_output(name="Yo:", prompt=prompt)
    
    def gpt_output(self, prompt):
        response = response.choice[0].message.content.strip()
        self.animate_gpt_output(name="ChatGPT", prompt=response)

    def run_prompt(self, event):
        # Usar el valor almacenado en text_value
        text = self.text_value
        self.chat.controls.append(CreateMessageTEXT("Yo:", text))
        self.chat.update()
        # Limpiar el TextField
        self.value = ""
        self.update()

        # Verificar si el token está disponible
        if not hasattr(self, 'token') or not self.token:
            print("Token no disponible")
            return
        
        # Enviar la solicitud a la API
        API_URL = 'http://localhost:8080/api/acv1/chatbot/'
        data = {'message': text}

        # try:
        #     # Usar una sesión para manejar cookies automáticamente
        #      with requests.Session() as session:
        #         session.headers.update({'Authorization': f'Token {self.token}'})
        #         response = session.post(API_URL, json=data)
        #         response.raise_for_status()  
        #         print(f"Cookies después de la primera solicitud: {session.cookies.get_dict()}") 
        #         mensaje_ia = response.json()
        #         print(mensaje_ia)
        #         self.chat.controls.append(CreateMessageGPT("Chat\nBOT:", mensaje_ia.get('response', 'No response')))
        #         self.chat.update()
        # except requests.exceptions.HTTPError as http_err:
        #     print(f"Error HTTP al obtener datos de la API: {http_err}")
        # except requests.exceptions.RequestException as req_err:
        #     print(f"Error al hacer la solicitud a la API: {req_err}")
        # except Exception as e:
        #     print(f"Error inesperado: {e}")
            
        # API_URL = 'http://localhost:8080/api/acv1/chatbot/'
        # data = {'message': text}

        try:
            response = requests.post(API_URL, json=data, headers={'Authorization': f'Token {self.token}'})
            response.raise_for_status()
            mensaje_ia = response.json()
            print(mensaje_ia)
            self.chat.controls.append(CreateMessageGPT("Chat\nBOT:", mensaje_ia.get('response', 'No response')))
            self.chat.update()
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP al obtener datos de la API: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Error al hacer la solicitud a la API: {req_err}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def on_text_change(self, event):
        self.text_value = event.control.value  # Actualizar el valor almacenado

def chatbot(page, app_state):
    page.padding = 0
    token = app_state.token
    print(token)

    if not token:
        # If no token, redirect to login
        page.controls.clear()
        login_view(page, app_state)
        page.update()
        return

    main = MainContentArea()
    prompt = Prompt(chat=main.chat)
    prompt.token = token  # Set the token here

    # Register the on_text_change event handler
    prompt.on_change = prompt.on_text_change

    btn_enviar = ft.TextButton(
        width=40,
        content=ft.Column(
            [
                ft.Icon(name=ft.icons.SEND_ROUNDED, color="#333333"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=lambda e: prompt.run_prompt(e)  # Trigger the prompt submission on button click
    )

    col_chat = ft.Container(
        content=ft.Column([main], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="transparent",
        padding=ft.padding.only(left=5, right=5, bottom=5),
        width=300,
    )

    row_prompt = ft.Container(
        content=ft.Row([prompt, btn_enviar], spacing=0, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(left=10, right=10),
        bgcolor=ft.colors.WHITE,
        width=330,
        alignment=ft.alignment.center,
        border_radius=50,
        border=ft.border.all(color="#333333"),
    )

    col_prompt = ft.Container(
        content=ft.Column([row_prompt], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=ft.colors.WHITE,
        padding=ft.padding.only(left=10, bottom=5, right=10),
        width=350,
        alignment=ft.alignment.center,
    )

    principal_container = ft.Container(
        content=ft.Column([col_chat], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.only(left=20, right=20, top=10),
        height=500,
        alignment=ft.alignment.center,
        border_radius=10,
        bgcolor=ft.colors.WHITE,
    )

    titulo_chart = ft.Text("ChatBOT", size=28, font_family="LTSaeada-5", weight=ft.FontWeight.BOLD, color=color_primary)

    row_titulo_chatbot = ft.Container(
        content=ft.Column([titulo_chart], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.only(top=20),
    )

    chatbot_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True,
    )

    row_button_prompt = ft.Container(
        content=ft.Column([col_prompt], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.only(left=10, top=10, right=10, bottom=30),
    )

    page.controls.append(row_titulo_chatbot)
    page.controls.append(chatbot_scrollable)
    page.controls.append(row_button_prompt)
    page.update()
