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
Este projeto explora a **expectativa de vida mundial**, investigando fatores socioeconômicos, de saúde e políticas públicas que impactam a longevidade. A análise é baseada em dados históricos e busca responder duas perguntas principais:

1. **Quais regiões têm os menores e maiores índices de longevidade em 2015?**
2. **Qual é a relação entre vacinação e longevidade?**
""")

# Carregamento de dados
@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()

# Pergunta 1: Quais regiões têm os menores e maiores índices de longevidade em 2015?
st.markdown("### 🧭 Quais regiões têm os menores e maiores índices de longevidade em 2015?")
st.markdown("*Utilizando os dados mais recentes do dataset.*")

def process_data(df):
    df_2015 = df[df['Year'] == 2015]
    selected_df = df_2015[['Country', 'Life expectancy', 'Adult Mortality', 'infant deaths', 'Population']]
    grouped_df = selected_df.groupby('Country', as_index=False).mean()
    top_long_life = grouped_df.nlargest(10, 'Life expectancy')
    bottom_long_life = grouped_df.nsmallest(10, 'Life expectancy')
    final_df = pd.concat([top_long_life, bottom_long_life]).reset_index(drop=True)
    return final_df

processed_df = process_data(df)
st.subheader("🌐 Top 10 Maiores e Menores Expectativas de Vida (2015)")
st.dataframe(processed_df)

st.markdown("""
Países como **Japão**, **Suíça** e **Suécia** lideram com expectativa de vida acima de 82 anos, indicando boa estrutura de saúde, saneamento e educação. 
Já países como **Serra Leoa**, **Chade** e **Angola** apresentam expectativa de vida abaixo de 55 anos, refletindo carência em serviços básicos.
""")

# Pergunta 2: Qual é a relação entre vacinação e longevidade?
st.markdown("### 💉 Qual é a relação entre vacinação e longevidade?")

def get_top_bottom_life_expectancy(df):
    df_2015 = df[df['Year'] == 2015]
    columns = ['Country', 'Life expectancy', 'Hepatitis B', 'Polio', 'Diphtheria']
    filtered_df = df_2015[columns]
    grouped = filtered_df.groupby('Country', as_index=False).mean(numeric_only=True)
    top5 = grouped.nlargest(5, 'Life expectancy').reset_index(drop=True)
    bottom5 = grouped.nsmallest(5, 'Life expectancy').reset_index(drop=True)
    return top5, bottom5

def show_vaccination_life_expectancy():
    top5, bottom5 = get_top_bottom_life_expectancy(df)

    st.subheader("🔝 Top 5 Países com Maior Expectativa de Vida e Taxas de Vacinação")
    st.dataframe(top5)

    st.subheader("🔻 Bottom 5 Países com Menor Expectativa de Vida e Taxas de Vacinação")
    st.dataframe(bottom5)

    st.markdown("""
Observamos que países com **maior expectativa de vida** também apresentam **altas taxas de vacinação**, especialmente contra doenças como **Poliomielite**, **Difteria** e **Hepatite B**.
Já países com **baixa longevidade** geralmente têm **índices vacinais abaixo da média**, o que contribui para altas taxas de mortalidade infantil e adulta.
""")

show_vaccination_life_expectancy()

# Intervalo de Confiança
def show_country_confidence_intervals(df):
    st.subheader("📊 Intervalos de Confiança da Expectativa de Vida por País (Ano Inicial vs Final)")

    country_stats = []
    for country, group in df.groupby('Country'):
        group = group.sort_values('Year')
        if len(group) >= 2:
            first_year = group.iloc[0]
            last_year = group.iloc[-1]
            values = [first_year['Life expectancy'], last_year['Life expectancy']]
            mean = np.mean(values)
            std = np.std(values, ddof=1)
            n = 2
            sem = std / np.sqrt(n)
            ci = t.interval(0.95, df=n - 1, loc=mean, scale=sem)
            country_stats.append({
                'Country': country,
                'Start Year': int(first_year['Year']),
                'End Year': int(last_year['Year']),
                'Start Life': first_year['Life expectancy'],
                'End Life': last_year['Life expectancy'],
                'Mean': mean,
                'CI Lower': ci[0],
                'CI Upper': ci[1]
            })

    stats_df = pd.DataFrame(country_stats).dropna()

    # Ordena pelos países com maior diferença entre começo e fim
    stats_df['Delta'] = stats_df['End Life'] - stats_df['Start Life']
    stats_df = stats_df.sort_values(by='Delta', ascending=False)

    fig = go.Figure()

    for i, row in stats_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Country'], row['Country']],
            y=[row['Start Life'], row['End Life']],
            mode='lines+markers',
            marker=dict(size=10),
            name=row['Country'],
            showlegend=False,
            line=dict(color='green' if row['Delta'] >= 0 else 'red')
        ))

    fig.update_layout(
        title="Mudança na Expectativa de Vida e Intervalo de Confiança (por País)",
        xaxis_title="Países",
        yaxis_title="Expectativa de Vida (anos)",
        template="plotly_white"
    )

    st.plotly_chart(fig)

    st.dataframe(stats_df[['Country', 'Start Year', 'End Year', 'Start Life', 'End Life', 'CI Lower', 'CI Upper']])


show_country_confidence_intervals(df)

# Finalização
st.markdown("""
### 📝 Conclusão
A partir das análises, observamos que **fatores como vacinação, mortalidade infantil e acesso a recursos básicos** estão diretamente ligados à expectativa de vida das populações. 
Esses insights ajudam a direcionar políticas públicas e ações de saúde para regiões com maior vulnerabilidade.
""")
