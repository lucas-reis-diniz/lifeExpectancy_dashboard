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

fig.add_traces(px.line(x=df_year["GDP"], y=predictions).data)

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
