import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()


st.subheader("Mapa Interativo da Expectativa de Vida")

country = st.selectbox("Selecione um país:", df["Country"].unique())

df_country = df[df["Country"] == country]

year = st.selectbox("Selecione o ano:", sorted(df_country["Year"].unique()))

df_year = df_country[df_country["Year"] == year]

fig = px.choropleth(df_year, locations="Country", locationmode="country names",
                    color="Life expectancy",
                    hover_name="Country",
                    color_continuous_scale="Viridis",
                    title=f"Expectativa de Vida em {country} no ano {year}")

st.plotly_chart(fig)


def generate_descriptions(df):
    descriptions = {}
    for country in df["Country"].unique():
        df_country = df[df["Country"] == country]
        life_exp_avg = df_country["Life expectancy"].mean()
        life_exp_min = df_country["Life expectancy"].min()
        life_exp_max = df_country["Life expectancy"].max()
        adult_mortality_avg = df_country["Adult Mortality"].mean()
        infant_deaths_avg = df_country["infant deaths"].mean()
        gdp_avg = df_country["GDP"].mean()
        population_avg = df_country["Population"].mean()
        schooling_avg = df_country["Schooling"].mean()

        description = (
            f"{country} possui uma expectativa de vida média de {life_exp_avg:.1f} anos, "
            f"variando entre {life_exp_min:.1f} e {life_exp_max:.1f} anos ao longo dos anos analisados. "
            f"A taxa média de mortalidade adulta é de {adult_mortality_avg:.1f} por 1000 habitantes, "
            f"enquanto a mortalidade infantil fica em torno de {infant_deaths_avg:.1f} mortes por ano. "
            f"O PIB médio registrado foi de {gdp_avg:.2f}, com uma população média de aproximadamente {population_avg:.0f} habitantes. "
            f"O nível médio de escolaridade no país foi de {schooling_avg:.1f} anos."
        )
        descriptions[country] = description
    return descriptions

descriptions = generate_descriptions(df)

if country in descriptions:
    st.markdown(f"**Descrição sobre o(a) {country}:** {descriptions[country]}")