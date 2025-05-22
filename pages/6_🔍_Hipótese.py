import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import ttest_ind, t
import plotly.graph_objects as go

st.set_page_config(page_title="Testes de Hipótese - Expectativa de Vida", layout="wide")
st.title("📊 Testes de Hipótese - Expectativa de Vida")

@st.cache_data
def load_data():
    return pd.read_csv("LifeExpectancy.csv")

df = load_data()

st.markdown("""
### 🎯 Objetivo
Aplicaremos **testes de hipótese estatísticos** para investigar se existem diferenças significativas na expectativa de vida com base em:

1. O nível de desenvolvimento do país (Desenvolvido vs. Em desenvolvimento)
2. A cobertura vacinal contra Hepatite B
""")

# ------------------------------
# Teste 1: Países Desenvolvidos vs Em Desenvolvimento
# ------------------------------
st.subheader("🧪 Teste 1: Diferença na Expectativa de Vida entre Países Desenvolvidos e em Desenvolvimento")

df_dev = df[df['Status'].notna() & df['Life expectancy'].notna()]
df_dev_grouped = df_dev.groupby("Status")["Life expectancy"]

developed = df_dev[df_dev['Status'] == "Developed"]["Life expectancy"]
developing = df_dev[df_dev['Status'] == "Developing"]["Life expectancy"]

st.markdown("""
**Hipóteses:**
- H₀: A média da expectativa de vida é a mesma nos dois grupos.
- H₁: A média da expectativa de vida é diferente entre países desenvolvidos e em desenvolvimento.
""")

stat1, p_value1 = ttest_ind(developed, developing, equal_var=False)

st.write(f"Estatística t: {stat1:.2f}")
st.write(f"Valor-p: {p_value1:.4f}")

if p_value1 < 0.05:
    st.success("Rejeitamos H₀: Há diferença significativa na expectativa de vida entre os grupos.")
else:
    st.info("Não rejeitamos H₀: Não há evidência suficiente para afirmar que as médias são diferentes.")

fig1 = px.box(df_dev, x="Status", y="Life expectancy",
              title="Distribuição da Expectativa de Vida por Nível de Desenvolvimento",
              labels={"Life expectancy": "Expectativa de Vida", "Status": "Status do País"})
st.plotly_chart(fig1)

# ------------------------------
# Teste 2: Vacinação Hepatite B
# ------------------------------
st.subheader("💉 Teste 2: Efeito da Vacinação contra Hepatite B na Expectativa de Vida")

df_vac = df[(df['Hepatitis B'].notna()) & (df['Life expectancy'].notna())]
high_vaccine = df_vac[df_vac['Hepatitis B'] >= 90]['Life expectancy']
low_vaccine = df_vac[df_vac['Hepatitis B'] < 90]['Life expectancy']

st.markdown("""
**Hipóteses:**
- H₀: A média da expectativa de vida é igual entre países com alta e baixa vacinação contra Hepatite B.
- H₁: Países com alta vacinação têm maior expectativa de vida.
""")

stat2, p_value2 = ttest_ind(high_vaccine, low_vaccine, alternative='greater', equal_var=False)

st.write(f"Estatística t: {stat2:.2f}")
st.write(f"Valor-p: {p_value2:.4f}")

if p_value2 < 0.05:
    st.success("Rejeitamos H₀: Alta vacinação está associada a maior expectativa de vida.")
else:
    st.info("Não rejeitamos H₀: Não há evidência suficiente de que a vacinação aumente a expectativa de vida.")

df_vac_grouped = df_vac.copy()
df_vac_grouped["Vacinação"] = np.where(df_vac_grouped["Hepatitis B"] >= 90, "Alta (≥ 90%)", "Baixa (< 90%)")
fig2 = px.box(df_vac_grouped, x="Vacinação", y="Life expectancy",
              title="Expectativa de Vida por Nível de Vacinação contra Hepatite B",
              labels={"Life expectancy": "Expectativa de Vida"})
st.plotly_chart(fig2)

# ------------------------------
# Conclusão Geral
# ------------------------------
st.markdown("""
### ✅ Conclusão Geral
- Há **diferença estatisticamente significativa** na expectativa de vida entre países desenvolvidos e em desenvolvimento.
- Países com **alta taxa de vacinação contra Hepatite B** também tendem a apresentar expectativa de vida **mais elevada**, com significância estatística.

Essas evidências reforçam a importância de políticas públicas voltadas à **saúde básica e imunização**.
""")

import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

# Configuração da página
st.set_page_config(page_title="Regressão Linear", layout="wide")
st.title("📈 Regressão Linear: PIB vs Expectativa de Vida")

st.markdown("""
Nesta análise, utilizamos **regressão linear simples** para investigar a relação entre o **Produto Interno Bruto (PIB)** e a **Expectativa de Vida**.  
A hipótese é: *"Países com maior PIB tendem a ter maior expectativa de vida."*
""")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df.dropna(subset=["GDP", "Life expectancy"])

df = load_data()

# Filtro por ano
year = st.selectbox("Selecione o ano para análise:", sorted(df["Year"].unique()))
df_year = df[df["Year"] == year]

# Regressão
X = df_year["GDP"]
y = df_year["Life expectancy"]
X = sm.add_constant(X)  # adiciona o intercepto
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# Gráfico
fig = px.scatter(df_year, x="GDP", y="Life expectancy",
                 labels={"GDP": "PIB", "Life expectancy": "Expectativa de Vida"},
                 title=f"Relação entre PIB e Expectativa de Vida em {year}")

fig.add_traces(px.line(x=df_year["GDP"], y=predictions, name="Regressão Linear").data)

st.plotly_chart(fig)

# Resultados
st.subheader("📋 Resumo da Regressão")
st.write(f"**Equação da reta:**  y = {model.params[1]:.4f} × PIB + {model.params[0]:.2f}")
st.write(f"**R² (coeficiente de determinação):** {model.rsquared:.3f}")
st.write(f"**p-valor do coeficiente do PIB:** {model.pvalues[1]:.4f}")

# Interpretação
st.subheader("🧠 Interpretação")
st.markdown(f"""
- O coeficiente positivo de {model.params[1]:.4f} indica que, em média, países com **PIB mais alto tendem a ter maior expectativa de vida**.
- O R² de **{model.rsquared:.3f}** indica que o modelo explica aproximadamente {model.rsquared * 100:.1f}% da variabilidade na expectativa de vida.
- O p-valor de **{model.pvalues[1]:.4f}** {'indica significância estatística' if model.pvalues[1] < 0.05 else 'não indica significância estatística'} para a variável PIB.

Esta análise reforça como aspectos econômicos estão associados à saúde populacional.
""")
