
#VARIABLES DE ENTORNO para URLs de API

#Si deseas probar en tu entorno local solo cambia estas dos URLs! ;)
API_BACK = 'http://34.135.120.63:8080'
API_WSP = 'http://34.135.120.63:3000'


#Solicitud para enviar mensaje WHATSAPP
SEND_WSP = f'{API_WSP}/send-message'

#Solicitud a chatBOT
SEND_CHATBOT = f'{API_BACK}/api/acv1/chatbot/'

#Iniciar sesión
HTTP_LOGIN = f'{API_BACK}/login/'

#Registrarse como nuevo usuario
HTTP_REGISTER = f'{API_BACK}/paciente/register/'

#Cerrar sesión
HTTP_LOGOUT = f"{API_BACK}/logout/"

#Realizar predicción para el objetivo 1 y Guardar
HTTP_OBJ_1 = f'{API_BACK}/api/acv1/create/'

#Realizar predicción para el objetivo 2
HTTP_OBJ_2 = f'{API_BACK}/api/acv2/create/'

#Realizar predicción para el objetivo 3
HTTP_OBJ_3 = f'{API_BACK}/api/acv3/create/'

#Obtener registros de predicciones del usuario autenticado
DATA_OBJ_1 = f'{API_BACK}/api/acv1/'