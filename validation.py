import flet as ft
from datetime import datetime
import re



def valid_textfield(page, col_control, text_control, control, icon):
    col_control.height=40
    text_control.value= "Campo válido"
    text_control.color=ft.colors.BLUE_300
    text_control.size=12
    control.border_color = ft.colors.BLUE_300
    control.focused_border_color = ft.colors.BLUE_300
    icon.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
    icon.color=ft.colors.BLUE_300
    icon.size=15
    page.update()

def error_textfield(page, col_control, text_control, control, icon, message):
    col_control.height=40
    text_control.value= message
    text_control.color=ft.colors.RED_300
    text_control.size=12
    control.border_color = ft.colors.RED_300
    control.focused_border_color = ft.colors.RED_300
    icon.name=ft.icons.ERROR_OUTLINE_ROUNDED
    icon.color=ft.colors.RED_300
    icon.size=15
    page.update()

def valid_radiobutton(page, col_control, text_control, control, icon):
    col_control.height=40
    text_control.value= "Campo válido"
    text_control.color=ft.colors.BLUE_300
    text_control.size=12
    control.border = ft.border.all(color=ft.colors.BLUE_300)
    icon.name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
    icon.color=ft.colors.BLUE_300
    icon.size=15
    page.update()

def error_radiobutton(page, col_control, text_control, control, icon, message):
    col_control.height=40
    text_control.value= message
    text_control.color=ft.colors.RED_300
    text_control.size=12
    control.border = ft.border.all(color=ft.colors.RED_300)
    icon.name=ft.icons.ERROR_OUTLINE_ROUNDED
    icon.color=ft.colors.RED_300
    icon.size=15
    page.update()

def validate_texto(page, value, tamano, col_control, text_control, control, icon):
            if not value:
                error_textfield(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            # Verificar si contiene solo letras y espacios
            elif re.match(r'^[A-Za-z ]+$', value):
                # Verificar la longitud
                if len(value) >= tamano:
                    error_textfield(page, col_control, text_control, control, icon, f"El campo no puede tener más de {tamano} caracteres.")
                    return f"El campo no puede tener más de {tamano} caracteres."
                else:
                    # Si no se encontró ningún error_textfield
                    valid_textfield(page, col_control, text_control, control, icon)
                    return None
            else:
                error_textfield(page, col_control, text_control, control, icon, "El campo puede contener solo letras y espacios.")
                return "El campo puede contener solo letras y espacios."
        

def validate_password(page, value, tamano, col_control, text_control, control, icon):
            if not value:
                error_textfield(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            elif not re.search(r'[\'\";%\(\)`\-&|=]', value):
                if  len(value) < 8:
                    error_textfield(page, col_control, text_control, control, icon, "La contraseña debe tener al menos 8 caracteres.")
                    return "La contraseña debe tener al menos 8 caracteres."
                elif len(value) > tamano:
                    error_textfield(page, col_control, text_control, control, icon, "La contraseña debe tener menos de 100 caracteres.")
                    return "La contraseña debe tener menos de 100 caracteres."
                else:
                    valid_textfield(page, col_control, text_control, control, icon)
                    return None
            else:
                error_textfield(page, col_control, text_control, control, icon, '''Caracteres no permitidos: ' " ; % ( ) ` - & | =''')
                return '''Caracteres no permitidos: ' " ; % ( ) ` - & | ='''


def validate_email(page, value, tamano, col_control, text_control, control, icon):
            if not value:
                error_textfield(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            
            # Verifica que el email contenga solo letras minúsculas, números, un solo @ y un solo punto
            elif re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', value):
                # Verifica que el email no tenga más de 100 caracteres
                if len(value) < tamano:     
                    # Verifica que el email tenga exactamente un símbolo de arroba
                    if value.count('@') != 1:
                        error_textfield(page, col_control, text_control, control, icon, "El correo debe contener un solo símbolo de arroba.")
                        return "El correo debe contener un solo símbolo de arroba."
                    else:
                        valid_textfield(page, col_control, text_control, control, icon)
                        return None
                else:
                    error_textfield(page, col_control, text_control, control, icon, "El campo no puede tener más de 100 caracteres.")
                    return "El campo no puede tener más de 100 caracteres."  
            else:
                error_textfield(page, col_control, text_control, control, icon, "Formato de correo incorrecto")
                return "Formato de correo incorrecto"
            

def validate_celular(page, value, col_control, text_control, control, icon):
            if not value:
                error_textfield(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            elif value.isdigit():
                if len(value) != 9:
                    error_textfield(page, col_control, text_control, control, icon, "El número de celular debe tener 9 dígitos.")
                    return "El número de celular debe tener 9 dígitos."
                else:
                    valid_textfield(page, col_control, text_control, control, icon)
                    return None
            else:
                error_textfield(page, col_control, text_control, control, icon, "El campo debe contener solo números.")
                return "El campo debe contener solo números."

def validate_radiobutton(page, value, col_control, text_control, control, icon):
            if not value:
                error_radiobutton(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            else:
                valid_radiobutton(page, col_control, text_control, control, icon)
                return None

def validate_fecha_nacimiento(page, value, col_control, text_control, control, icon):
            if not value:
                error_textfield(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            try:
                fecha = datetime.strptime(value, '%Y-%m-%d')
                edad = (datetime.now() - fecha).days // 365
                if edad < 1:
                    error_textfield(page, col_control, text_control, control, icon, "La edad debe ser mayor o igual a 1 año.")
                    return "La edad debe ser mayor o igual a 1 año."
                else:
                    valid_textfield(page, col_control, text_control, control, icon)
                    return None
            except ValueError:
                error_textfield(page, col_control, text_control, control, icon, "El formato de la fecha debe ser YYYY-MM-DD.")
                return "El formato de la fecha debe ser YYYY-MM-DD."

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def validate_intervalo(page, value, col_control, text_control, control, icon, min, max):
            if not value:
                error_textfield(page, col_control, text_control, control, icon, "El campo no puede estar vacío.")
                return "El campo no puede estar vacío."
            # Verifica que el email contenga solo letras minúsculas, números, un solo @ y un solo punto
            elif is_float(value):
                if float(value) < min or float(value) > max:
                    error_textfield(page, col_control, text_control, control, icon, f"Ingrese un valor numérico entre {min} y {max}.")
                    return f"Ingrese un valor numérico entre {min} y {max}."
                else:
                    valid_textfield(page, col_control, text_control, control, icon)
                    return None 
            else:
                error_textfield(page, col_control, text_control, control, icon, "Ingrese solo números enteros o decimales.")
                return "Ingrese solo números enteros o decimales."

