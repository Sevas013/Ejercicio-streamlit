import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard de Ventas de Videojuegos")

opcion = st.sidebar.selectbox(
    "Selecciona una de las siguientes opciones",
    ["Cargar archivo", "Análisis exploratorio", "Indicadores", "Gráficas"]
)

if opcion == "Cargar archivo":
    st.header("1. Carga de archivo CSV")
    archivoCSV = st.file_uploader("Elige un archivo CSV", type=["csv"])
    if archivoCSV is not None:
        st.session_state.df = pd.read_csv(archivoCSV)
        st.write(st.session_state.df)

elif opcion == "Análisis exploratorio":
    st.header("2. Exploración de Datos")
    if "df" in st.session_state:
        df = st.session_state.df
        st.subheader("Dimensiones del dataset:")
        st.write(f"Filas: **{df.shape[0]}**, Columnas: **{df.shape[1]}**")
        st.subheader("Nombres de las columnas:")
        st.write(list(df.columns))
        st.subheader("Primeras 10 filas:")
        st.write(df.head(10))
        st.subheader("Estadísticas descriptivas:")
        st.write(df.describe())
    else:
        st.warning("ERROR: No puedes explorar un archivo si no lo has subido a 'Cargar archivo'.") 

elif opcion == "Indicadores":
    st.header("3. Indicadores Clave")
    if "df" in st.session_state:
        df = st.session_state.df

        # Indicador 1: Variedad de juegos   
        variedad_juegos = df["Name"].nunique()
        st.metric("Videojuegos únicos", variedad_juegos, help="Cantidad de títulos distintos en el dataset.")

        # Indicador 2: Plataformas distintas
        plataformas = df["Platform"].nunique()
        st.metric("Plataformas", plataformas, help="Cantidad de plataformas en las que se publicaron juegos.")

        # Indicador 3: Videojuego más vendido globalmente
        juego_top = df.loc[df["Global_Sales"].idxmax()]["Name"]
        ventas_top = df["Global_Sales"].max()
        st.metric("Juego más vendido (Global)", juego_top, f"{ventas_top} millones")

        # Indicador 4: Ventas totales globales
        ventas_global = df["Global_Sales"].sum()
        st.metric("Ventas globales totales", f"{ventas_global:.2f} millones")

        # Indicador 5: Año con mayores ventas
        ventas_anual = df.groupby("Year")["Global_Sales"].sum()
        best_year = int(ventas_anual.idxmax())
        ventas_best = ventas_anual.max()
        st.metric("Año con más ventas", best_year, f"{ventas_best:.2f} millones")
    else:
        st.warning("ERROR: No puedes explorar un archivo si no lo has subido a 'Cargar archivo'.")

elif opcion == "Gráficas":
    st.header("4. Visualizaciones")

    if "df" in st.session_state:
        df = st.session_state.df

        # Gráfica 1: Ventas globales por género
        st.subheader("Ventas Globales por Género")
        genero_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
        fig1, ax1 = plt.subplots()
        genero_sales.plot(kind="bar", ax=ax1)
        ax1.set_xlabel("Género")
        ax1.set_ylabel("Ventas Globales (millones)")
        st.pyplot(fig1)

        # Gráfica 2: Top 10 juegos por ventas en Norteamérica
        st.subheader("Top 10 Juegos por Ventas en Norteamérica")
        top10_na = df.nlargest(10, "NA_Sales").set_index("Name")["NA_Sales"]
        fig2, ax2 = plt.subplots()
        top10_na.plot(kind="barh", ax=ax2)
        ax2.set_xlabel("Ventas NA (millones)")
        st.pyplot(fig2)

        # Gráfica 3: Evolución de ventas globales por año
        st.subheader("Evolución de Ventas Globales por Año")
        ventas_year = df.groupby("Year")["Global_Sales"].sum()
        fig3, ax3 = plt.subplots()
        ventas_year.plot(ax=ax3, marker="o")
        ax3.set_xlabel("Año")
        ax3.set_ylabel("Ventas Globales (millones)")
        st.pyplot(fig3)

    else:
        st.warning("ERROR: No puedes explorar un archivo si no lo has subido a 'Cargar archivo'.")