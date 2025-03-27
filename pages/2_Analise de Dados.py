import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import binom
from scipy.stats import poisson
from plotnine import *

st.set_page_config(page_title="Analise dos Dados", layout="wide")

st.title("Analise dos Dados")

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

st.markdown("""
O histograma acima mostra a distribuição da expectativa de vida nos diferentes países e anos do dataset.

**O que podemos observar?**
- A maioria dos valores de expectativa de vida está concentrada entre 50 e 80 anos.
- Podemos identificar se há países com valores extremamente baixos ou altos.
- A presença de um **boxplot** na parte superior ajuda a visualizar outliers (valores muito fora da curva).
""" )

st.subheader("Expectativa de vida Por País")

country = st.selectbox("Selecione um país:", df["Country"].unique())

df_country = df[df["Country"] == country]

fig = px.line(df_country, x="Year", y="Life expectancy", markers=True,
              title=f"Expectativa de vida ao Longo dos Anos em {country}",
              labels={"Life expectancy": "Expectativa de Vida", "Year": "Anos"})
st.plotly_chart(fig)