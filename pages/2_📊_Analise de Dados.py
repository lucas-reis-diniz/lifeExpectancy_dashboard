import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import stats
from scipy.stats import t
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Análise dos Dados", layout="wide")

st.title("Análise dos Dados")

st.markdown("""
### 🏥 Sobre este Projeto  
Este projeto analisa a **expectativa de vida mundial** ao longo dos anos, explorando como diferentes fatores impactam a longevidade em diversas regiões.  

📌 **Por que escolhemos este dataset?**  
- A expectativa de vida é um **indicador chave do desenvolvimento humano**.  
- Permite **comparar países e analisar tendências ao longo do tempo**.  
- Podemos investigar **o impacto de fatores como saúde, economia e políticas públicas**.  

📌 **Impacto desta análise**  
- Compreender padrões globais pode ajudar governos e ONGs a **tomar decisões baseadas em dados**.  
- Pode revelar **desigualdades regionais e fatores que contribuem para maior longevidade**.  
""")

@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()

st.subheader("📊 Estatísticas Descritivas")

st.markdown("""
Aqui temos um **resumo estatístico das variáveis numéricas** do dataset.  
Essa tabela nos mostra medidas importantes, como:  

- **Média**: Valor médio da expectativa de vida e outras variáveis.  
- **Desvio Padrão**: Indica o quão dispersos os dados estão em relação à média.  
- **Mínimo e Máximo**: Valores extremos observados no dataset.  
- **Quartis (25%, 50%, 75%)**: Dividem os dados em percentis, ajudando a entender a distribuição.  
""")

st.write(df.describe())

st.markdown("""
📌 **Principais observações:**  
- A **média da expectativa de vida** é aproximadamente **X anos** (*substituir pelo valor real*).  
- O **desvio padrão** mostra que os dados variam consideravelmente entre países.  
- O **percentil 25%** indica que **25% dos países têm uma expectativa de vida abaixo de Y anos**.  
- O **percentil 75%** mostra que **os 25% com maior expectativa de vida estão acima de Z anos**.  

Essas estatísticas nos ajudam a compreender **a dispersão dos dados e padrões gerais**, o que será útil para as próximas análises.  
""")

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

options = st.multiselect(
    "Escolha as análises que deseja visualizar:",
    [
     "Doenças por Região",
     "Correlação entre PIB e Expectativa de Vida",
     "Impacto da Vacinação na Expectativa de Vida"
    ]
)

if "Doenças por Região" in options:
    st.subheader("Distribuição de Doenças por Região")

    disease_options = [
        "Hepatitis B", "Measles ", "Polio", "Diphtheria ", " HIV/AIDS", "infant deaths", "under-five deaths "
    ]
    disease = st.selectbox("Selecione uma doença para visualizar:", disease_options)

    df = df.dropna(subset=["Country", disease])  # Remove valores nulos na coluna de país e da doença selecionada
    df["Country"] = df["Country"].astype(str)  # Garante que a coluna "Country" seja string

    valid_countries = px.data.gapminder()["country"].unique()
    df = df[df["Country"].isin(valid_countries)]  # Mantém apenas países válidos

    if df.empty:
        st.warning("Nenhum dado válido para exibir no mapa. Verifique os filtros aplicados.")
    else:
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

st.subheader("📏 Intervalo de Confiança para Expectativa de Vida")

st.markdown("""
Os **intervalos de confiança** são usados para estimar um intervalo dentro do qual acreditamos que a **média real** da expectativa de vida se encontra.  

Isso nos ajuda a entender **a variação dos dados ao longo dos anos** e a fazer previsões mais seguras.  

Neste caso, utilizamos um **intervalo de confiança de 95%**, ou seja, há **95% de chance da média real da expectativa de vida estar dentro desse intervalo**.  
""")

life_expectancy = df["Life expectancy"].dropna()  # Removendo valores NaN

# Calcular média e desvio padrão
mean_life = np.mean(life_expectancy)
std_life = np.std(life_expectancy, ddof=1)  # ddof=1 para amostra

n = len(life_expectancy)
sem = std_life / np.sqrt(n)  # Erro padrão da média
confidence_interval = t.interval(0.95, df=n-1, loc=mean_life, scale=sem)

x = np.linspace(mean_life - 4*std_life, mean_life + 4*std_life, 1000)
y = stats.norm.pdf(x, mean_life, std_life)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color="black", linewidth=2, label="Distribuição Normal")

x_confidence = np.linspace(confidence_interval[0], confidence_interval[1], 300)
y_confidence = stats.norm.pdf(x_confidence, mean_life, std_life)
ax.fill_between(x_confidence, y_confidence, color="blue", alpha=0.4, label="95% IC")

ax.fill_between(x[x < confidence_interval[0]], y[x < confidence_interval[0]], color="purple", alpha=0.4, label="2.5% Inferior")
ax.fill_between(x[x > confidence_interval[1]], y[x > confidence_interval[1]], color="purple", alpha=0.4, label="2.5% Superior")

ax.axvline(confidence_interval[0], color="black", linestyle="dashed")
ax.axvline(confidence_interval[1], color="black", linestyle="dashed")

ax.set_title("Distribuição da Expectativa de Vida com Intervalo de Confiança de 95%", fontsize=14)
ax.set_xlabel("Expectativa de Vida (anos)", fontsize=12)
ax.set_ylabel("Densidade de Probabilidade", fontsize=12)
ax.legend()

st.pyplot(fig)

st.write(f"**Média da Expectativa de Vida:** {mean_life:.2f} anos")
st.write(f"**Intervalo de Confiança de 95%:** [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}] anos")
