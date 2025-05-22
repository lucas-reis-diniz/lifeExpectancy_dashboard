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
- O número positivo de {model.params[1]:.4f} mostra que, de forma geral, países com um PIB (Produto Interno Bruto) mais alto costumam ter uma expectativa de vida maior.
- O valor de R² é {model.rsquared:.3f}, o que quer dizer que o modelo consegue explicar cerca de {model.rsquared * 100:.1f}% das diferenças na expectativa de vida entre os países.
- O p-valor é {model.pvalues[1]:.4f}, o que {'mostra que a relação entre PIB e expectativa de vida é estatisticamente confiável' if model.pvalues[1] < 0.05 else 'indica que a relação pode ser apenas coincidência'}.

Esta análise reforça como aspectos econômicos estão associados à saúde populacional.
""")
