import flet as ft
import requests
from urlsapi import API_WSP

""" 
Estimado/a {{1}},

{{2}}, tras revisar los resultados de sus pruebas, {{3}}

{{4}}

_*Parámetros evaluados:*_

_*Género:*_ {{5}}
_*Edad:*_ {{6}}
_*Hipertensión:*_ {{7}}
_*Cardiopatía:*_ {{8}}
_*Tipo de Trabajo:*_ {{9}}
_*Estado Fumador:*_ {{10}}
_*Nivel de Glucosa Promedio:*_ {{11}}
_*ICM:*_ {{12}}

Atentamente,
NeuroIA - ACV 

http://localhost:3000/send-message
"""




def message_whatsapp(page, nombre_paciente, mensaje1, mensaje2, telefono, w_genero, w_edad, w_hipertension, w_cardiopatia, w_trabajo, w_fumador, w_glucosa, w_imc):

           
            """ #OPCIÓN 1:
            # Definir el token de acceso de Facebook y el identificador de número de teléfono
            token = 'EAB0AiAJlz8MBOZB8vplepCZBj5TMxwTSgtOzFz5ZA97OklZCumfoZCuQm1ZAVjUq8pVhw4ZCeljnWfHKSxMytaul9mGgXWJf8xkcaVEi3uMGZA8bPbRKLXE9iaSFrUh6oc31Nejamd8DQAHj97KDZAC7tleXu7EAngho1ZCQbdPEYSobCILwzjTdQmZBGOAY43FDClTKGxGIHac6rVmJlxddY0ZD'
            
            id_numero_telefono = '369274782941272'

            #Obtener número de celular del cliente
            #celular = app_state.paciente_data.get('celular', 'Celular')
            #telefono_envia = f"51{celular}"
            telefono_envia = telefono

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Enviar mensaje de plantilla
            data_mensaje = {
                'messaging_product': 'whatsapp',
                'to': telefono_envia,
                'type': 'template',
                'template': {
                    'name': 'diagnostico',
                    'language': {
                        'code': 'es'
                    },
                'components': [
                    {
                        'type': 'body',
                        'parameters': [
                            {'type': 'text', 'text': nombre_paciente},
                            {'type': 'text', 'text': mensaje1},
                            {'type': 'text', 'text': mensaje2},
                            {'type': 'text', 'text': ' '},
                            {'type': 'text', 'text': w_genero},
                            {'type': 'text', 'text': w_edad},
                            {'type': 'text', 'text': w_hipertension},
                            {'type': 'text', 'text': w_cardiopatia},
                            {'type': 'text', 'text': w_trabajo},
                            {'type': 'text', 'text': w_fumador},
                            {'type': 'text', 'text': w_glucosa},
                            {'type': 'text', 'text': w_imc},
                        ]
                    }
                ]
                }
            }
            response_mensaje = requests.post(f'https://graph.facebook.com/v20.0/{id_numero_telefono}/messages', json=data_mensaje, headers=headers)
            if response_mensaje.status_code == 200:
                page.dialog = ft.AlertDialog(title=ft.Text("✅ El resultado del diagnóstico ha sido enviado a su whatsapp.",color="#333333", text_align=ft.TextAlign.CENTER, size=15),
                                bgcolor=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(10))
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠️ El resultado del diagnóstico no pudo ser enviado a su whatsapp debido a un problema inesperado.",color="#333333", text_align=ft.TextAlign.CENTER, size=15),
                                bgcolor=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(10))
                print(f"Error: {response_mensaje.status_code} - {response_mensaje.text}") """



            #OPCIÓN 2: Se necesita el servido en NODEJS
            mensaje=f"*RESULTADO DE DIAGNÓSTICO:*\n\nEstimado/a {nombre_paciente},\n\n{mensaje1}, tras revisar los resultados de sus pruebas, {mensaje2}\n\n_*Parámetros evaluados:*_\n\n_*Género:*_ {w_genero}\n_*Edad:*_ {w_edad}\n_*Hipertensión:*_ {w_hipertension}\n_*Cardiopatía:*_ {w_cardiopatia}\n_*Tipo de Trabajo:*_ {w_trabajo}\n_*Estado Fumador:*_ {w_fumador}\n_*Nivel de Glucosa Promedio:*_ {w_glucosa}\n_*ICM:*_ {w_imc}\n\nAtentamente,\nNeuroIA - ACV"
            url = f'{API_WSP}/send-message'
            data = {'number': telefono, 'message': mensaje}
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                page.dialog = ft.AlertDialog(title=ft.Text("✅ El resultado del diagnóstico ha sido enviado a su whatsapp.",color="#333333", text_align=ft.TextAlign.CENTER, size=15),
                                bgcolor=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(10))
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠️ El resultado del diagnóstico no pudo ser enviado a su whatsapp debido a un problema inesperado.",color="#333333", text_align=ft.TextAlign.CENTER, size=15),
                                bgcolor=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(10))
                print(f"Error: {response.status_code} - {response.text}")
            
            page.dialog.open = True
            page.update()



