import streamlit as st

st.set_page_config(page_title="Dashboard Expectativa de Vida por Região", layout="wide")

st.title("🌍 Dashboard Expectativa de Vida por Região")

st.markdown("""
Este dashboard foi desenvolvido para explorar e analisar **dados da expectativa de vida** em diferentes países ao longo dos anos.  
A partir de análises interativas, podemos entender como **fatores socioeconômicos e de saúde impactam a longevidade da população**.
""")

st.image("global-life-expectancy.jpg", use_container_width=True)

st.subheader("📊 Sobre os Dados")
st.markdown("""
Os dados utilizados neste projeto foram coletados de diversas fontes globais, como **OMS (Organização Mundial da Saúde) e ONU**.  
Eles incluem informações sobre **expectativa de vida, PIB, mortalidade infantil, taxas de vacinação e outros fatores determinantes** da longevidade.
""")

st.subheader("🎯 Objetivos do Dashboard")
st.markdown("""
Neste dashboard, você poderá:
- 📈 **Analisar a evolução da expectativa de vida ao longo dos anos** em diferentes países.  
- 🏥 **Investigar o impacto de doenças e vacinação** na longevidade.  
- 💰 **Explorar a relação entre fatores econômicos (PIB) e a expectativa de vida**.  
- 🌎 **Comparar regiões e identificar padrões globais e desigualdades**.  
""")

st.subheader("❓ Perguntas que podemos responder")
st.markdown("""
🔹 Como a expectativa de vida mudou ao longo do tempo?  
🔹 Qual é a relação entre vacinação e longevidade?  
🔹 Países com maior PIB apresentam maior expectativa de vida?  
🔹 Quais regiões têm os menores e maiores índices de longevidade?  
🔹 A mortalidade infantil está relacionada à expectativa de vida?  
""")

st.subheader("🔍 Conclusões e Insights")
st.markdown("""
- 🌎 **Países desenvolvidos** geralmente possuem maior expectativa de vida devido a melhores condições de saúde, saneamento e nutrição.  
- 💉 **A vacinação** desempenha um papel essencial na redução da mortalidade infantil e aumento da longevidade.  
- 💰 **Fatores econômicos** como PIB estão fortemente correlacionados à longevidade, mas não são os únicos determinantes.  
""")

st.subheader("🚀 Explore os Dados!")
st.write("Navegue pelas páginas do dashboard para visualizar gráficos interativos e obter insights valiosos.")
if st.button("Ir para Análises 📊"):
    st.switch_page("pages/2_📊_Analise de Dados.py")
