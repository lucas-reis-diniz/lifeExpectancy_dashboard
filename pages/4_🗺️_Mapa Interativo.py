import streamlit as st
import pandas as pd
import plotly.express as px
import imageio
import os

@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()

st.subheader("Mapa Interativo da Expectativa de Vida 🌍")

# Criando o mapa com todos os países
year = st.slider("Selecione um ano:", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=int(df["Year"].median()))

df_year = df[df["Year"] == year]

fig = px.choropleth(df_year, locations="Country", locationmode="country names",
                    color="Life expectancy",
                    hover_name="Country",
                    color_continuous_scale="Viridis",
                    title=f"Expectativa de Vida no Ano {year}")

st.plotly_chart(fig)

# Gerar animação em GIF
st.subheader("🎥 Timelapse da Expectativa de Vida")

generate_gif = st.button("Gerar Timelapse")

if generate_gif:
    gif_frames = []
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    years = sorted(df["Year"].unique())

    for y in years:
        df_year = df[df["Year"] == y]
        fig = px.choropleth(df_year, locations="Country", locationmode="country names",
                            color="Life expectancy",
                            hover_name="Country",
                            color_continuous_scale="Viridis",
                            title=f"Expectativa de Vida no Ano {y}")

        file_path = os.path.join(temp_dir, f"frame_{y}.png")
        fig.write_image(file_path)
        gif_frames.append(imageio.imread(file_path))

    gif_path = "life_expectancy_timelapse.gif"
    imageio.mimsave(gif_path, gif_frames, duration=200.0)  # Criar GIF

    st.image(gif_path, caption="Timelapse da Expectativa de Vida", use_container_width=True)

    # Limpeza dos frames temporários
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
