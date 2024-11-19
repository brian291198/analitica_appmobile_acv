import flet as ft
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from menubar import menubar
from login import login_view

# Function to generate the cluster plot
def generar_grafico_clusters(X, clusters):
    plt.figure(figsize=(6, 4))
    scatter = plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis')
    plt.colorbar(scatter)
    plt.title('Gráfico de Clusters')
    plt.xlabel('Total vendido')
    plt.ylabel('Frecuencia de Ventas')

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)  # Go back to the start of the file
    plt.close()  # Close the plot to free memory
    return img_data

#  -------------------- 
# Load the data from Excel
df = pd.read_excel('assets/BoletasVentaFiltrada.xlsx')
df['Fecha Venta'] = pd.to_datetime(df['Fecha Venta'])
df['Mes_Año'] = df['Fecha Venta'].dt.to_period('M')

# Aggregate data
product_stats = df.groupby(['Tienda', 'Marca', 'Grupo', 'Genero', 'Descripcion Producto','TALLA','COLOR','Mes_Año']).agg({
    'Cantidad': 'sum',  
    'Fecha Venta': ['min', 'max', 'nunique'], 
    'Ext Precio Vta': 'sum'  
}).reset_index()

product_stats.columns = ['Tienda', 'Marca', 'Grupo', 'Genero', 'Descripcion Producto','TALLA','COLOR', 'Mes_Año', 'Total Vendido', 
                        'Primera Venta', 'Última Venta', 'Frecuencia Ventas', 'Ingresos Totales']

# Create the view in Flet
def objetive2_view(page, app_state):
    if not app_state.token:
        # If no token, redirect to login
        page.controls.clear()
        login_view(page, app_state)
        page.update()
        return
    
    # Color and style variables
    color = "#404040"
    color_primary = "#007ACC"
    border_radius = 10

    # Filter data based on selected store and group
    def filtrar_datos(tienda):
        filtered_data = product_stats[(product_stats['Tienda'] == tienda) ]
        X = filtered_data[['Total Vendido', 'Frecuencia Ventas', 'Ingresos Totales']]
        return X
    
    # Function to update the scatter plot and interpretation
    def actualizar_grafico(e):
        tienda_seleccionada = dropdown_tienda.value
        grupo_seleccionado = dropdown_grupo.value

        if tienda_seleccionada:
            # Filter and scale the data
            X_filtered = filtrar_datos(tienda_seleccionada)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_filtered)

            # Apply KMeans
            kmeans = KMeans(n_clusters=4, random_state=0)
            clusters = kmeans.fit_predict(X_scaled)

            # Assign clusters to product_stats for later filtering
            filtered_data = product_stats[(product_stats['Tienda'] == tienda_seleccionada)].copy()
            filtered_data['Cluster'] = clusters

            # Store filtered_data in the app state to access it later in mostrar_info_cluster
            app_state.filtered_data = filtered_data

            # Generate the plot and update the image
            img_data = generar_grafico_clusters(X_scaled, clusters)
            img_base64 = base64.b64encode(img_data.getvalue()).decode('utf-8')
            img_control.src_base64 = img_base64

            # Clear previous buttons and add new ones based on clusters
            cluster_buttons.controls.clear()
            for i in range(kmeans.n_clusters):
                button = ft.ElevatedButton(
                    text=f"Cluster {i + 1}",
                    on_click=lambda e, cluster=i: mostrar_info_cluster(cluster),
                    width=100,
                    color=color_primary
                )
                cluster_buttons.controls.append(button)

            page.update()

    # Function to display information about a specific cluster
    def mostrar_info_cluster(cluster_index):
        # Filter products belonging to the selected cluster
        cluster_data = app_state.filtered_data[app_state.filtered_data['Cluster'] == cluster_index]
        
        # Remove duplicate products
        cluster_data = cluster_data.drop_duplicates(subset=['Descripcion Producto'])

        # Sort the data by 'Ingresos Totales' in descending order
        cluster_data = cluster_data.sort_values(by='Ingresos Totales', ascending=False)

        # Build the text to display products in the selected cluster with auto-incrementing numbers
        product_list_text = "\n".join([f"{i + 1}. {row['Descripcion Producto']} | Ingresos: {row['Ingresos Totales']:.2f}" 
                                        for i, (_, row) in enumerate(cluster_data.iterrows())])

        interpretacion_text.value = f"Detalles del Cluster {cluster_index + 1}:\n{product_list_text}"
        page.update()


    cluster_buttons = ft.Row(spacing=5)

        
    #variables para colores
    color="#404040"
    color_hint="#C3C7CF"

    txt_grupo=ft.Row(
            [
                ft.Icon(name=ft.icons.CATEGORY, color=color_hint),
                ft.Text("Grupo", color=color)            
            ]
        )
    # Campo de búsqueda
    txt_busqueda = ft.TextField(
            hint_text="Buscar grupo...",
            hint_style=ft.TextStyle(color=color_hint),  # Color del texto de sugerencia
            text_style=ft.TextStyle(color=color),  # Color del texto que escribe el usuario
            prefix_icon=ft.icons.SEARCH,  # Ícono de búsqueda antes del texto
            on_change=lambda e: actualizar_dropdown(e.control.value, dropdown_grupo,product_stats['Grupo'].unique())
        )
    
    txt_tienda=ft.Row(
            [
                ft.Icon(name=ft.icons.STORE, color=color_hint),
                ft.Text("Tiendas", color=color)            
            ]
        )
    # Create dropdowns for Store and Group
    dropdown_tienda = ft.Dropdown(
        options=[ft.dropdown.Option(tienda) for tienda in product_stats['Tienda'].unique()],
        on_change=actualizar_grafico,
        hint_text="Selecciona una Tienda",
        color="#6dbadc",
    )

    def actualizar_dropdown(busqueda, dropdown, opciones):
            dropdown.options = [ft.dropdown.Option(opcion) for opcion in product_stats['Grupo'].unique() if busqueda.lower() in opcion.lower()]
            dropdown.update() 


    dropdown_grupo = ft.Dropdown(
        options=[ft.dropdown.Option(grupo) for grupo in product_stats['Grupo'].unique()],
        on_change=actualizar_grafico,
        hint_text="Selecciona un Grupo",
        color="#6dbadc",
    )

    # Create an image container
    img_control = ft.Image(width=300, height=200)

    

    # Create a Text element for interpretation
    interpretacion_text = ft.Text(value="", size=12, color=color)

    # Create the page layout
    col_volver = ft.Container()

    col_grupos=ft.Container(content=ft.Column([
                txt_grupo,
                txt_busqueda,
                dropdown_grupo,
                ]
            ), width=300,
            padding=15,
            border=ft.border.all(color="#cccccc"),
            border_radius=10 
            #border=ft.border.all()
            )  
    
    col_tienda = ft.Container(
        content=ft.Column([txt_tienda,dropdown_tienda]),
        width=300,
        padding=15,
        border=ft.border.all(color="#cccccc"),
        border_radius=10 
    )

    col_grafico = ft.Container(
        content=ft.Column([img_control]),
        width=300,
        margin=20,
        alignment=ft.alignment.center
    )

    col_interpretacion = ft.Container(
        content=ft.Column([interpretacion_text]),
        width=300,
        margin=20,
    )

    row_grupo=ft.Container(content=ft.Column([
                col_grupos,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        #border=ft.border.all()
        )

    row_tienda=ft.Container(content=ft.Column([
                col_tienda,
        ], spacing=0
        ),
        padding=ft.padding.only(left=10, top=10, right=10),  
        alignment=ft.alignment.center,
        border=ft.border.all()
        )

    # Main layout
    principal_container = ft.Container(
        content=ft.Column([col_volver, row_grupo,row_tienda, col_grafico,cluster_buttons, col_interpretacion]),
        width=360,
        alignment=ft.alignment.center,
    )
    
    objetive1_scrollable = ft.ListView(
        controls=[principal_container],
        expand=True, 
        )

    # Add the main container to the page
    page.controls.append(objetive1_scrollable)
    page.update()


# Function to go back to the home screen
def accion_volver_home(e, page, app_state):
    page.controls.clear()
    menubar(page, app_state)
    page.update()
