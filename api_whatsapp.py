import flet as ft
import requests


def message_whatsapp(page, nombre_paciente, mensaje1, mensaje2, telefono):

            # Definir el token de acceso de Facebook y el identificador de número de teléfono
            token = 'EAB0AiAJlz8MBO5eBqjqT7nDeYNgkxEEkvtmzurSKb3ePat0tSDxZA8pevZByPUfb6FDcQkgVZAku4gJyJlu4UgwBy60pRLw4Vq5v6WULoncW9oEX1vsbpzW0oGxIK59qPwwpeWjUd1G41QJSKqmA6qFZADiZBFLOb4LXUucFOCZAOgfxL5PWzvGQVaF4Wym6I5C5OFfuACSZBFXQch75YsZD'
            id_numero_telefono = '369274782941272'
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
                page.dialog = ft.AlertDialog(title=ft.Text("⚠️ El resultado del diganóstico no pudo ser enviado a su whatsapp debido a un problema inesperado.",color="#333333", text_align=ft.TextAlign.CENTER, size=15),
                                bgcolor=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(10))
                print(f"Error: {response_mensaje.status_code} - {response_mensaje.text}")
            
            page.dialog.open = True
            page.update()

