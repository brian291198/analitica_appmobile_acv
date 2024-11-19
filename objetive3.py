import flet as ft
import requests
from login import login_view
from datetime import datetime
from validation import validate_radiobutton, validate_intervalo
import time
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from styles import color, color_hint, color_primary, color_secondary, color_hovered, color_check, color_error
from menubar import menubar
from urlsapi import HTTP_OBJ_2
from sklearn.preprocessing import StandardScaler
from io import BytesIO
import base64
from mlxtend.frequent_patterns import apriori, association_rules
import joblib
import seaborn as sns


# Crear la vista en Flet
def objetive3_view(page, app_state):
    if not app_state.token:
        # Si no hay token, redirigir al inicio de sesión
            page.controls.clear()
            login_view(page, app_state)
            page.update()
            return
    #Obtener token
    token =app_state.token
    page.padding=0

    def accion_volver_home(e, page, app_state):
        page.controls.clear()
        menu_bar=menubar(page, app_state)
        page.controls.append(menu_bar)
        page.controls.append(ft.Container(height=1, bgcolor=color_hint, margin=ft.margin.only(left=20, right=20)))
        app_state.show_home()
        page.update()
            
    #variables para colores
    color="#404040"
    color_hint="#C3C7CF"


    #boton en texto -> < VOLVER
    texto_volver = ft.TextButton(
        on_click=lambda e: accion_volver_home(e, page, app_state),
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.ARROW_BACK_IOS_SHARP, color=ft.colors.WHITE, size=10),
                ft.Container(width=5),
                ft.Text("Volver", color=ft.colors.WHITE)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),     
        )
    
    #titulo del objetivo 1
    txt_objetivo = ft.Text("MARKET BASKET ANALYSIS", style=ft.TextStyle(size=16, weight="bold", color=ft.colors.WHITE))
            
    # Breve descripcion del tema
    txt_descripcion = ft.Text("Algoritmo de minería de datos que identifica conjuntos de ítems frecuentes", style=ft.TextStyle(size=14, color=ft.colors.WHITE))
    imagen_principal = ft.Container(
                        content=ft.Column(controls=[
                            ft.Image(src=f"/objetivo3.png", width=100, height=100, repeat=ft.ImageRepeat.NO_REPEAT,)
                    ]),width=100)
            
    # Titulo de formulario
    txt_formulario = ft.Text("REGLAS ASOCIADAS", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)

    #----------------- Modelo Apriori ---------------------

    df = joblib.load('assets/df_sinfiltrar.joblib')
    print(df)
    # Función para actualizar la tabla con todas las reglas

    # Función para cerrar el diálogo
    def close_dialog(page):
        page.dialog.open = False
        page.update()


        
    def update_table(rules):
        rows = []

        # Verificar si rules está vacío
        if rules.empty:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Container(
                        ft.Text("Sin datos", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=12),  # Cambiar a un tamaño adecuado como un número
                        height=100, expand=True
                    )),
                    ft.DataCell(ft.Container()),
                    ft.DataCell(ft.Container()),  # Celda vacía para coincidir con el número de columnas
                    #ft.DataCell(ft.Container()),  # Celda vacía para coincidir con el número de columnas
                ])
            )
        else:
            for _, row in rules.iterrows():
                antecedents = ', '.join(list(row['antecedents']))
                consequents = ', '.join(list(row['consequents']))
                
                # Crear el botón con el ícono de información
                #eye_icon = ft.IconButton(
                #    icon=ft.icons.INFO,  # Cambia EYE por INFO
                #    tooltip="Ver detalles",
                #    on_click=lambda e, antecedents=antecedents, consequents=consequents, df=df: show_details(antecedents, consequents,df)
                #)

                rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Container(ft.Text(antecedents, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD), padding=ft.padding.all(2), height=100)),
                        ft.DataCell(ft.Container(ft.Text(consequents, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD), padding=ft.padding.all(2), height=100)),
                        ft.DataCell(ft.Container(ft.Text(f"{row['confidence'] * 100:.2f}%", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD), padding=ft.padding.all(2), height=100, expand=True)),
                        #ft.DataCell(eye_icon)  # Agregar el botón a la fila
                    ])
                )

        # Actualizar la tabla con las filas creadas
        table.rows = rows
        page.update()

    # Crear las columnas para la tabla de reglas de asociación
    columns = [
        ft.DataColumn(
            ft.Text('Producto\nComprado', 
                    color=ft.colors.BLACK, 
                    weight=ft.FontWeight.BOLD),
            on_sort=lambda e: print("Ordenar por 'Producto Comprado'")
        ),
        ft.DataColumn(
            ft.Text("Producto\nSugerido", 
                    color=ft.colors.BLACK, 
                    weight=ft.FontWeight.BOLD),
            on_sort=lambda e: print("Ordenar por 'Producto Sugerido'")
        ),
        ft.DataColumn(
            ft.Text("Probabilidad\n de Compra", 
                    color=ft.colors.BLACK, 
                    weight=ft.FontWeight.BOLD),
            on_sort=lambda e: print("Ordenar por 'Probabilidad de Compra'")
        ),

    ]

    # Titulo de Resultados
    txt_resultados = ft.Text("RESULTADOS", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)

    # Tabla inicial
    table = ft.DataTable(
        columns=columns,
        rows=[],
        column_spacing=8,  # Ajustar espaciado entre columnas
        heading_text_style=ft.TextStyle(size=11),  # Ajustar tamaño del texto de las cabeceras
        data_text_style=ft.TextStyle(size=10),     # Ajustar tamaño del texto de las celdas
    
    )

    txt_grupo=ft.Row(
            [
                ft.Icon(name=ft.icons.CATEGORY, color=color_hint),
                ft.Text("Grupo", color=color, weight="bold")            
            ]
        )
    
    # Campo de búsqueda
    txt_busqueda = ft.TextField(
        hint_text="Buscar grupo...",
        hint_style=ft.TextStyle(color=color_hint, size=13),  # Color y tamaño del texto de sugerencia
        text_style=ft.TextStyle(color=color, size=13),  # Color y tamaño del texto que escribe el usuario
        prefix_icon=ft.icons.SEARCH,  # Ícono de búsqueda antes del texto
        on_change=lambda e: actualizar_dropdown(e.control.value, item_selection, df['Grupo'].unique()),  # Cambiado para buscar en los grupos
        height=45  # Ajusta la altura del campo
    )

    item_selection = ft.Dropdown(
        label="Elija",
        options=[ft.dropdown.Option(item) for item in df['Grupo'].unique()],  # Cambiado para opciones de grupos
        width=160,  # Ajusta el ancho
        color="#6dbadc",
        suffix_icon=ft.icons.ARROW_DROP_DOWN,  # Ícono de desplegable
        height=45,  # Ajusta la altura del Dropdown
        text_style=ft.TextStyle(size=12)  # Ajusta el tamaño de la letra a 12
    )


    def actualizar_dropdown(busqueda, dropdown, opciones):
            dropdown.options = [ft.dropdown.Option(opcion) for opcion in opciones if busqueda.lower() in opcion.lower()]
            dropdown.update() 

    # Función para mostrar las reglas de asociación según el grupo seleccionado
    def show_associated_rules(e):
        selected_item = item_selection.value
        print(selected_item)
        
        # Aplicar Apriori a todos los productos
        basket = df.groupby(['NroRecibo', 'Descripcion Producto'])['Cantidad'].sum().unstack(fill_value=0)
        basket = basket.astype(bool).astype(int)
        print(basket)

        # Aplicar Apriori y generar reglas para todos los productos
        frequent_itemsets = apriori(basket, min_support=0.001, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.001)
        print(rules)


    # Filtrar reglas para mostrar solo antecedentes que contengan productos del grupo seleccionado
        if selected_item:
            # Obtener solo los productos que pertenecen al grupo seleccionado
            products_in_group = df[df['Grupo'] == selected_item]['Descripcion Producto'].unique()
            # Filtrar reglas donde los antecedentes contengan solo productos del grupo seleccionado
            filtered_rules = rules[rules['antecedents'].apply(lambda x: any(item in products_in_group for item in x))]
        else:
            filtered_rules = rules  # Sin filtro si no hay selección

        print(filtered_rules)
        print(filtered_rules[['antecedents', 'consequents', 'confidence']])

        # Actualizar la tabla con las reglas filtradas
        update_table(filtered_rules)

        # Mostrar mensaje si no hay reglas para generar el gráfico
        if filtered_rules.empty:
            # Mostrar un mensaje flotante (snack bar) en la parte inferior de la pantalla
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Nada que generar. No hay registros.")))
        else:
            # Generar el gráfico de calor si hay reglas
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Generando Imagen!! Espere ....")))
            generar_grafico_calor(filtered_rules)
            page.update()
                
    def generar_grafico_calor(rules, metric='confidence'):
        # Convertir antecedentes y consecuentes en strings
        rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        
        # Crear una matriz de calor basada en la métrica seleccionada (confidence en este caso)
        heatmap_data = rules.pivot_table(index='antecedents_str', columns='consequents_str', values=metric, fill_value=0)
        # Crear el mapa de calor
        plt.figure(figsize=(20, 15))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Confidence'},
                    linewidths=.5, linecolor='black', annot_kws={"size": 10})
        plt.title('Mapa de Calor de las Reglas de Asociación', fontsize=16)
        plt.xlabel('Consecuentes', fontsize=12)
        plt.ylabel('Antecedentes', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(rotation=0, fontsize=12)
        plt.tight_layout()
        #plt.show()
        # Guardar la figura como imagen
        plt.savefig("heatmap_rules.png")
        plt.show()


    # Actualiza el botón para mostrar las reglas de asociación del grupo seleccionado
    show_associations_button = ft.ElevatedButton(
        text="Filtrar",
        on_click=show_associated_rules,
        bgcolor="#808080",
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    )

    # Función para manejar la descarga
    def download_action(e):
        print('Descargando Imagen')


    # Botón para descargar
    download_button = ft.ElevatedButton(
        text="Descargar",
        on_click=download_action,  # Función que maneja la descarga
        bgcolor="#e78ead",
        color=ft.colors.WHITE,
        icon=ft.icons.DOWNLOAD,  # Icono de descarga
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
        tooltip="Descargar Grafico de Calor"  # Tooltip
    )

        # Contenedor para el botón de descarga con margen
    download_container = ft.Container(
        content=download_button,
        margin=ft.Margin(left=0, top=10, right=0, bottom=10)   # Aquí se aplica el margen superior
    )


    # Colocar ambos en una fila con alineación
    row_combo_boton = ft.Row(
        [
            item_selection,  # Combo a la izquierda
            ft.Container(expand=True),  # Espacio flexible para empujar el botón a la derecha
            show_associations_button  # Botón a la derecha
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Distribuye los elementos en los extremos
    )

    # Inicializar tabla con todas las reglas
    # update_table(rules)
    

    #CONTAINERS PARA SEPARAR COLUMNAS DE ELEMENTOS
    col_volver=ft.Container(content=ft.Row([
            texto_volver
        ], alignment=ft.MainAxisAlignment.END
        ), width=360, 
        margin=2, 
        #border=ft.border.all()
        )
            
    col_derecha=ft.Container(content=ft.Column([
                txt_objetivo,
                txt_descripcion
            ]), width=200, margin=ft.margin.only(top=2, bottom=2), )
            
            
    col_izquierda=ft.Container(content=ft.Column([
                imagen_principal
        ]), width=100)
            
    col_titulo_form=ft.Container(content=ft.Column([
            txt_formulario
        ]
        ), width=300, 
        alignment=ft.alignment.center, 
        margin=ft.margin.only(top=4, bottom=3),
        )
    
    col_resultados_form=ft.Container(content=ft.Column([
            txt_resultados
        ]
        ), width=300, 
        alignment=ft.alignment.center, 
        margin=ft.margin.only(top=4, bottom=3),
        )
    
    col_grupos=ft.Container(content=ft.Column([
                txt_grupo,
                txt_busqueda,
                row_combo_boton,
                
            ]
            ), width=300,
            padding=10,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )    
    
    col_table_data = ft.Container(
        content=ft.Column(
            [
                table
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centra el contenido en el eje principal
        ),
        width=300,
        padding=2,
        border=ft.border.all(color="#cccccc"),
        border_radius=10,
        alignment=ft.alignment.center,  # Centra el contenido del Container
    ) 

        
            
#----------------------------------------------------------------------------------------------------------------------------------------------  

    #CONTAINERS PARA SEPARAR FILAS DE ELEMENTOS
    row_volver_container=ft.Container(content=ft.Column([
            col_volver
    ]
    ), 
    border=None,
    )

    row_titulo_container=ft.Container(content=ft.Row([
            col_derecha,
            col_izquierda
    ], spacing=0, alignment=ft.MainAxisAlignment.CENTER
    ), 
    border=None,
    )

    row_titulo_form=ft.Container(content=ft.Column([
            col_titulo_form
    ]
    ), 
    #width=360,
    alignment=ft.alignment.center,
    #border=ft.border.all()
    )

    row_resultados_form=ft.Container(content=ft.Column([
            col_resultados_form
    ]
    ), 
    #width=360,
    alignment=ft.alignment.center,
    #border=ft.border.all()
    )
    
    row_grupo=ft.Container(content=ft.Column([
                col_grupos,
        ], spacing=0
        ),
        padding=ft.padding.only(top=10, bottom=10, left=8, right=8),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

    row_resultado=ft.Container(content=ft.Column([
            col_table_data
    ]
    ),
    alignment=ft.alignment.center,
    width=300,
    )

    #CONTAINER PRINCIPAL
    row_superior=ft.Container(content=ft.Column([
            row_volver_container,
            row_titulo_container,              
    ],spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    ), 
    bgcolor=color_primary,
    padding=ft.padding.only(left=20, top=10, bottom=20, right=20),
    )

    row_form=ft.Container(content=ft.Column([
                    row_titulo_form,
                    row_grupo,
                    row_resultados_form,
                    row_resultado],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
                    ),
                    bgcolor=ft.colors.WHITE,
                    #margin=,
                    #padding=2,
                    width=450,
                    alignment=ft.alignment.center,
                    border_radius=20
                    )


    principal_container=ft.Container(content=ft.Column([
                    row_superior,                    
                    row_form,
                    download_container

            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
            ), 
            width=450,
            alignment=ft.alignment.center,
            #border=ft.border.all(),
            )
            
    objetive2_scrollable = ft.ListView(
            controls=[principal_container],
            expand=True,  # Permitir que el contenedor ocupe todo el espacio disponible
            )

            #page.controls.clear()
    page.controls.append(objetive2_scrollable)
    page.update()






