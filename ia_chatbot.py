import flet as ft
import openai
import time
from styles import color, color_hint, color_primary, color_secondary, color_hovered



def main_style():
    return{
        "width": 290,
        "height": 420,
        "bgcolor": "white",
    }

""" def prompt_style():
    return{
        "width": 300,
        "height": 40,
        "border_color":"#333333",
        "content_padding": 15,
        "cursor_color":"#333333",
        "color":"#333333"
    } """
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
        "height":20,
    }

# main content area class
class MainContentArea(ft.Container):
    def __init__(self) -> None:
        super().__init__(**main_style())
        self.chat = ft.ListView(
            expand=True,
            height=200,
            spacing=0,
            auto_scroll=True,
        )
        self.content = self.chat

# before pushing text to UI - create a class that generates the UI for the actual text prompts
class CreateMessage(ft.Column):
    def __init__(self, name: str, message: str):
        self.name = name #show's which prompt is whos
        self.message = message
        self.text = ft.Text(self.message, color="#333333")
        super().__init__(spacing=4)
        self.controls = [ft.Text(self.name,color="#333333", opacity=0.4), self.text]

# user input class
class Prompt(ft.TextField):
    def __init__(self, chat: ft.ListView):
        super().__init__(**prompt_style(), on_submit=self.run_prompt)
        #need access to main chat area - from MaincontentArea class
        self.chat = chat

    def animate_text_output(self, name:str, prompt:str):
        word_list: list = []
        msg = CreateMessage(name, "")

        #list(prompt) => we deconstruct the prompt text into sepreate characters, and loop over them
        for word in list(prompt):
            word_list.append(word)
            msg.text.value = "".join(word_list)
            self.chat.update()
            time.sleep(0.008)



    def user_output(self, prompt):
        #we can test the message UI now
        msg = CreateMessage("Yo:", prompt)
        self.chat.controls.append(msg)
        self.chat.update()
    
    """ def user_output(self, prompt):
        self.animate_text_output(name="Yo:", prompt=prompt)
     """
    
    def gpt_output(self, prompt):
        # the following is the basic response to get chat GPT answers
        """ response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}]
        )
        response = response.choice[0].message.content.strip()
        self.animate_text_output(name="ChatGPT", prompt=response) """


    # method: run all methods when started
    def run_prompt(self, event):
        # set the value of the user prompt
        text = event.control.value
                
        #disabling input field can also be added
        self.value = ""# clear entry
        self.update()


        # first, we output the user prompt
        self.user_output(prompt=text)

        # second, we display GPT output
        self.gpt_output(prompt=text)

def chatbot(page, app_state):


    btn_enviar=ft.TextButton(
                    width=40,
                    content=ft.Column(
                        [
                            ft.Icon(name=ft.icons.SEND_ROUNDED, color="#333333"),
                        ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

    main = MainContentArea()

    #main.chat => the ListView we created in that class...
    prompt = Prompt(chat=main.chat)

    """   page.add(
        ft.Text("ChatGPT en Flet", size = 28, color=ft.colors.BLUE_600, font_family="LTSaeada-5"),
        main,
        ft.Divider(height=6, color="transparent"),
        prompt,
    ) """


    col_chat=ft.Container(content=ft.Column([
            main,      
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ), 
        bgcolor="transparent",
        padding=ft.padding.only(left=5, top=10, right=5, bottom=5),
        width=300,
        )

    row_prompt=ft.Container(content=ft.Row([
                prompt,
                btn_enviar
                
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Centrar horizontalmente
                ),
                padding=ft.padding.only(left=10, right=10),
                bgcolor=ft.colors.WHITE,
                width=330,
                alignment=ft.alignment.center,
                border_radius=50,
                border=ft.border.all(color="#333333"),
                )
    col_prompt=ft.Container(content=ft.Column([
                row_prompt
                
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Centrar horizontalmente
                ),
                bgcolor=ft.colors.WHITE,
                padding=ft.padding.only(left=10, bottom=5, right=10),
                width=350,
                alignment=ft.alignment.center,
                )

    principal_container=ft.Container(content=ft.Column([
                col_chat,
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
        ), 
        margin=ft.margin.only(left=20, right=20, top=10),
        padding=ft.padding.only(top=10),
        height=500,
        alignment=ft.alignment.center,
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        )
    

    titulo_chart=ft.Text("ChatBOT", size=28,font_family="LTSaeada-5", weight=ft.FontWeight.BOLD, color=color_primary)

    row_titulo_chatbot=ft.Container(content=ft.Column([
        titulo_chart,
    ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,),padding=ft.padding.only(top=20, bottom=10),)

    chatbot_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
        )
    row_button_prompt=ft.Container(content=ft.Column([
        col_prompt
    ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,),margin=ft.margin.only(left=10, top=10, right=10, bottom=30),)

    #page.controls.clear()
    page.controls.append(row_titulo_chatbot)
    page.controls.append(chatbot_scrollable)
    page.controls.append(row_button_prompt)
    page.update()

