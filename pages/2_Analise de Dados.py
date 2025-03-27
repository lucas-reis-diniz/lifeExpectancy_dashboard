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

st.subheader("Perguntas que podemos responder com esses dados")

st.markdown("""
- Qual é a expectativa de vida média global?
- Como a expectativa de vida mudou ao longo dos anos em diferentes países?
- Países desenvolvidos têm uma expectativa de vida maior do que os em desenvolvimento?
- Existe uma relação entre PIB e expectativa de vida?
- Como os índices de vacinação impactam a expectativa de vida?
- Qual é a taxa de mortalidade infantil nos países com menor expectativa de vida?
""")

st.subheader("Distribuição da Expectativa de Vida")

fig = px.histogram(df, x="Life expectancy", nbins=30, title="Histograma da Expectativa de Vida",
                   labels={"Life expectancy": "Expectativa de Vida"}, opacity=0.7, marginal="box")
st.plotly_chart(fig)

st.subheader("Expectativa de Vida Por País")

country = st.selectbox("Selecione um país:", df["Country"].unique())

df_country = df[df["Country"] == country]

fig = px.line(df_country, x="Year", y="Life expectancy", markers=True,
              title=f"Expectativa de vida ao longo dos anos em {country}",
              labels={"Life expectancy": "Expectativa de Vida", "Year": "Anos"})
st.plotly_chart(fig)

# Mapa Coroplético para visualizar doenças por região
st.subheader("Distribuição de Doenças por Região")

# Filtros para escolher a doença
disease_options = [
    "Hepatitis B", "Measles", "Polio", "Diphtheria", "HIV/AIDS", "infant deaths", "Under-five deaths"
]
disease = st.selectbox("Selecione uma doença para visualizar:", disease_options)

# Preprocessamento para evitar erros no mapa
df = df.dropna(subset=["Country", disease])  # Remove valores nulos na coluna de país e da doença selecionada
df["Country"] = df["Country"].astype(str)  # Garante que a coluna "Country" seja string

# Lista de países reconhecidos pelo Plotly
valid_countries = px.data.gapminder()["country"].unique()
df = df[df["Country"].isin(valid_countries)]  # Mantém apenas países válidos

if df.empty:
    st.warning("Nenhum dado válido para exibir no mapa. Verifique os filtros aplicados.")
else:
    # Criando o mapa
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=disease,
        hover_name="Country",
        animation_frame="Year",
        color_continuous_scale="Reds",
        title=f"Distribuição de {disease} ao longo dos anos"
    )
    st.plotly_chart(fig)
