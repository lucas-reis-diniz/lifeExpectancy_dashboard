import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise dos Dados", layout="wide")

st.title("Análise dos Dados")

@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()

st.subheader("Estatísticas Descritivas")
st.write(df.describe())

st.subheader("Classificação das Variáveis")

data_types = {
    "Country": "Qualitativo Nominal",
    "Year": "Quantitativo Discreto",
    "Status": "Qualitativo Nominal",
    "Life expectancy": "Quantitativo Contínuo",
    "Adult Mortality": "Quantitativo Contínuo",
    "infant deaths": "Quantitativo Discreto",
    "Alcohol": "Quantitativo Contínuo",
    "Hepatitis B": "Quantitativo Discreto",
    "Measles": "Quantitativo Discreto",
    "BMI": "Quantitativo Contínuo",
    "Under-five deaths": "Quantitativo Discreto",
    "Polio": "Quantitativo Discreto",
    "Total expenditure": "Quantitativo Contínuo",
    "Diphtheria": "Quantitativo Discreto",
    "HIV/AIDS": "Quantitativo Contínuo",
    "GDP": "Quantitativo Contínuo",
    "Population": "Quantitativo Discreto",
    "Thinness 1-19 years": "Quantitativo Contínuo",
    "Thinness 5-9 years": "Quantitativo Contínuo",
    "Income composition of resources": "Quantitativo Contínuo",
    "Schooling": "Quantitativo Contínuo",
}

df_types = pd.DataFrame(list(data_types.items()), columns=["Variável", "Tipo de Dado"])
st.write(df_types)

st.subheader("Selecione a Análise Desejada")

options = st.multiselect(
    "Escolha as análises que deseja visualizar:",
    ["Distribuição da Expectativa de Vida",
     "Expectativa de Vida por País",
     "Doenças por Região",
     "Correlação entre PIB e Expectativa de Vida",
     "Impacto da Vacinação na Expectativa de Vida"]
)

if "Distribuição da Expectativa de Vida" in options:
    st.subheader("Distribuição da Expectativa de Vida")
    fig = px.histogram(df, x="Life expectancy", nbins=30, title="Histograma da Expectativa de Vida",
                       labels={"Life expectancy": "Expectativa de Vida"}, opacity=0.7, marginal="box")
    st.plotly_chart(fig)

if "Expectativa de Vida por País" in options:
    st.subheader("Expectativa de Vida por País")
    country = st.selectbox("Selecione um país:", df["Country"].unique())
    df_country = df[df["Country"] == country]
    fig = px.line(df_country, x="Year", y="Life expectancy", markers=True,
                  title=f"Expectativa de Vida ao Longo dos Anos em {country}",
                  labels={"Life expectancy": "Expectativa de Vida", "Year": "Ano"})
    st.plotly_chart(fig)

if "Doenças por Região" in options:
    st.subheader("Doenças por Região")
    disease = st.selectbox("Selecione uma doença:", [" Measles", "Hepatitis B", "Polio", " Diphtheria", " HIV/AIDS"])
    fig = px.choropleth(df, locations="Country", locationmode="country names",
                        color=disease, hover_name="Country",
                        animation_frame="Year",
                        color_continuous_scale="Reds",
                        title=f"Distribuição de {disease} ao longo dos anos")
    st.plotly_chart(fig)

if "Correlação entre PIB e Expectativa de Vida" in options:
    st.subheader("Correlação entre PIB e Expectativa de Vida")
    fig = px.scatter(df, x="GDP", y="Life expectancy", trendline="ols",
                     title="Relação entre PIB e Expectativa de Vida",
                     labels={"GDP": "PIB", "Life expectancy": "Expectativa de Vida"})
    st.plotly_chart(fig)

if "Impacto da Vacinação na Expectativa de Vida" in options:
    st.subheader("Impacto da Vacinação na Expectativa de Vida")
    vaccine = st.selectbox("Selecione uma vacina:", ["Hepatitis B", "Polio", "Diphtheria"])
    fig = px.scatter(df, x=vaccine, y="Life expectancy", trendline="ols",
                     title=f"Relação entre {vaccine} e Expectativa de Vida",
                     labels={vaccine: "Taxa de Vacinação (%)", "Life expectancy": "Expectativa de Vida"})
    st.plotly_chart(fig)
