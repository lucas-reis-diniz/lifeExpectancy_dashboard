import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import t, norm
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Análise da Expectativa de Vida", layout="wide")

# Título principal
st.title("🌍 Análise da Expectativa de Vida Mundial")

# Introdução
st.markdown("""
### 📊 Contexto do Projeto
Este projeto explora a **expectativa de vida mundial**, investigando fatores socioeconômicos, de saúde e políticas públicas que impactam a longevidade. A análise é baseada em dados históricos e busca responder perguntas relevantes sobre os padrões globais.
""")

st.write("Selecionamos duas perguntas principais para direcionar a analise de dados e assim obter conclusões mais objetivas sobre as informações.")

st.markdown("### Quais regiões têm os menores e maiores índices de longevidade em 2015?")
st.markdown("*dados mais recentes*")


# Carregamento de dados
@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()


def process_data(df):

    df_2015 = df[df['Year'] == 2015]
    # Selecionar colunas relevantes
    selected_df = df_2015[['Country', 'Year', 'Life expectancy', 'Adult Mortality', 'infant deaths', 'Population']]
    
    # Agrupar por país e tirar média
    grouped_df = selected_df.groupby('Country', as_index=False).mean()
    
    # Selecionar os 10 países com maior e menor expectativa de vida
    top_long_life = grouped_df.nlargest(10, 'Life expectancy')
    bottom_long_life = grouped_df.nsmallest(10, 'Life expectancy')
    
    # Concatenar os dois DataFrames
    final_df = pd.concat([top_long_life, bottom_long_life]).reset_index(drop=True)
    
    return final_df

processed_df = process_data(df)
st.dataframe(processed_df)  # Exibe as primeiras linhas da tabela processada


def calculate_general_averages(df):
    # Selecionar apenas as colunas relevantes
    selected_df = df[['Life expectancy', 'Adult Mortality', 'infant deaths']]

    # Calcular média ignorando valores ausentes
    averages = selected_df.mean(numeric_only=True)

    # Renomear para visualização
    averages_df = averages.reset_index()
    averages_df.columns = ['Indicador', 'Média Geral']
    
    return averages_df

def show_general_averages():
    df = load_data()
    avg_df = calculate_general_averages(df)
    st.subheader("📊 Média Geral de Expectativa de Vida e Mortalidades (Todos os Anos e Países)")
    st.dataframe(avg_df)

# Chamar no app
show_general_averages()

st.write("""Ao analisarmos os dados de 2015, ficou claro que os países com maior expectativa de vida estavam principalmente na Europa e Ásia desenvolvida — como Japão, Suíça e Suécia —, onde as pessoas viviam, em média, mais de 82 anos. Já os países com menor longevidade, como Serra Leoa, Chade e Angola, estavam concentrados na África Subsaariana, com expectativa de vida abaixo dos 55 anos.

Essas diferenças mostram como o acesso à saúde, saneamento e qualidade de vida faz toda a diferença. Onde há mais estrutura, as pessoas vivem mais. Onde faltam recursos básicos, os desafios ainda são enormes para garantir uma vida longa e saudável.

""")

st.markdown("### Qual é a relação entre vacinação e longevidade?")

def get_top_bottom_life_expectancy(df):
    # Filtrar apenas o ano de 2015
    df_2015 = df[df['Year'] == 2015]

    # Selecionar colunas relevantes
    columns = [
        'Country', 'Life expectancy', 'Adult Mortality', 'infant deaths', 'Population',
        'Hepatitis B', 'Polio', 'Diphtheria', 'Measles', 'HIV/AIDS'
    ]
    filtered_df = df_2015[columns]

    # Agrupar por país e tirar média (caso haja duplicatas)
    grouped = filtered_df.groupby('Country', as_index=False).mean(numeric_only=True)

    # Top 5 maiores e menores expectativa de vida
    top5 = grouped.nlargest(5, 'Life expectancy').reset_index(drop=True)
    bottom5 = grouped.nsmallest(5, 'Life expectancy').reset_index(drop=True)

    return top5, bottom5

def show_vaccination_life_expectancy():
    st.subheader("🧬 Vacinação e Longevidade em 2015")

    df = load_data()
    top5, bottom5 = get_top_bottom_life_expectancy(df)

    st.subheader("Top 5 Países com Maior Expectativa de Vida")
    st.dataframe(top5)

    st.subheader("Bottom 5 Países com Menor Expectativa de Vida")
    st.dataframe(bottom5)

# Executar no app
show_vaccination_life_expectancy()

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
