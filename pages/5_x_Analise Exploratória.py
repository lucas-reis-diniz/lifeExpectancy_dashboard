import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import t, norm
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Análise Exploratória", layout="wide")

# Título principal
st.title("🌍 Análise Exploratória dos Dados")

# Introdução
st.markdown("""
### 📊 Explore os Dados!
            Nessa página você poderá explorar todos os dados obtidos através do nosso banco de dados. Selecione países e categorias de sua escolha para fazer a análise!
""")

# Carregamento de dados
@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()

# Distribuição da Expectativa de Vida
st.subheader("📊 Distribuição da Expectativa de Vida")
st.markdown("""
Este gráfico mostra como a expectativa de vida está distribuída globalmente.
""")
fig = px.histogram(df, x="Life expectancy", nbins=30, title="Histograma da Expectativa de Vida",
                   labels={"Life expectancy": "Expectativa de Vida"}, opacity=0.7, marginal="box")
st.plotly_chart(fig)

st.write("(Adicionar texto explicando os dados fora do padrão apresentado)")

# Análise por país
st.subheader("🌎 Evolução da Expectativa de Vida por País")
country = st.selectbox("Selecione um país:", df["Country"].unique())
df_country = df[df["Country"] == country]
fig = px.line(df_country, x="Year", y="Life expectancy", markers=True,
              title=f"Expectativa de vida ao longo dos anos em {country}",
              labels={"Life expectancy": "Expectativa de Vida", "Year": "Anos"})
st.plotly_chart(fig)

# Seleção de análise personalizada
st.subheader("📌 Análises Relacionadas")
st.markdown("""
Selecione abaixo as perguntas que deseja responder com os dados.
""")
options = st.multiselect(
    "Escolha as análises:",
    ["Correlação entre PIB e Expectativa de Vida", "Impacto da Vacinação na Expectativa de Vida", "Distribuição de Doenças por Região"]
)

if "Correlação entre PIB e Expectativa de Vida" in options:
    st.subheader("💰 Expectativa de Vida vs. PIB")
    st.markdown("""
    Aqui exploramos a relação entre o Produto Interno Bruto (PIB) e a expectativa de vida. A tendência geralmente mostra que países com maior PIB têm uma população com maior longevidade.
    """)
    fig = px.scatter(df, x="GDP", y="Life expectancy", trendline="ols",
                     title="Relação entre PIB e Expectativa de Vida",
                     labels={"GDP": "PIB", "Life expectancy": "Expectativa de Vida"})
    st.plotly_chart(fig)

if "Impacto da Vacinação na Expectativa de Vida" in options:
    st.subheader("💉 Impacto da Vacinação na Expectativa de Vida")
    vaccine = st.selectbox("Escolha uma vacina:", ["Hepatitis B", "Polio", "Diphtheria"])
    st.markdown(f"""
    Analisamos como a vacinação contra {vaccine} influencia a expectativa de vida. Países com altas taxas de vacinação geralmente apresentam melhores índices de longevidade.
    """)
    fig = px.scatter(df, x=vaccine, y="Life expectancy", trendline="ols",
                     title=f"Relação entre {vaccine} e Expectativa de Vida",
                     labels={vaccine: "Taxa de Vacinação (%)", "Life expectancy": "Expectativa de Vida"})
    st.plotly_chart(fig)

if "Distribuição de Doenças por Região" in options:
    st.subheader("🦠 Distribuição de Doenças por Região")
    disease = st.selectbox("Selecione uma doença:", ["Hepatitis B", "Measles ", "Polio", "Diphtheria ", "HIV/AIDS", "infant deaths", "under-five deaths "])
    st.markdown(f"""
    A análise abaixo mostra a distribuição da doença **{disease}** em diferentes países ao longo dos anos.
    """)
    fig = px.choropleth(
        df.dropna(subset=["Country", disease]),
        locations="Country", locationmode="country names",
        color=disease, hover_name="Country", animation_frame="Year",
        color_continuous_scale="Reds",
        title=f"Distribuição de {disease} ao longo dos anos"
    )
    st.plotly_chart(fig)

# Intervalo de Confiança
st.subheader("📏 Intervalo de Confiança da Expectativa de Vida")
st.markdown("""
Utilizamos um intervalo de confiança de 95% para estimar onde a verdadeira média da expectativa de vida se encontra.
""")
life_expectancy = df["Life expectancy"].dropna()
mean_life = np.mean(life_expectancy)
std_life = np.std(life_expectancy, ddof=1)
n = len(life_expectancy)
sem = std_life / np.sqrt(n)
confidence_interval = t.interval(0.95, df=n-1, loc=mean_life, scale=sem)

fig = go.Figure()
x = np.linspace(mean_life - 4*std_life, mean_life + 4*std_life, 1000)
y = norm.pdf(x, mean_life, std_life)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribuição Normal', line=dict(color='#1f77b4', width=2)))
fig.add_trace(go.Scatter(x=[confidence_interval[0], confidence_interval[1]],
                          y=[0, 0], mode='lines', name='Intervalo de Confiança', line=dict(color='red', dash='dash')))
fig.update_layout(title="Distribuição da Expectativa de Vida com Intervalo de Confiança de 95%",
                  xaxis_title="Expectativa de Vida (anos)", yaxis_title="Densidade de Probabilidade",
                  template="plotly_white")
st.plotly_chart(fig)

st.write(f"**Média da Expectativa de Vida:** {mean_life:.2f} anos")
st.write(f"**Intervalo de Confiança de 95%:** [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}] anos")

st.write("Caculo para o intervalo de confiança com 95% de certeza com base nos dados")
