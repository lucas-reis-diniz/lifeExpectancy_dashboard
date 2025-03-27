import streamlit as st

st.set_page_config(page_title="Dashboard Expectativa de Vida por Região", layout="wide")

st.title("Dashboard Expectativa de Vida por Região")

st.write("Este dashboard foi desenvolvido para explorar e analisar dados relacionados à expectativa de vida em diferentes países ao longo dos anos. Aqui, você poderá visualizar tendências, comparar fatores que influenciam a longevidade e entender a relação entre variáveis como mortalidade infantil, vacinação, PIB e outros indicadores socioeconômicos.")

st.image("global-life-expectancy.jpg")

st.subheader("O que você encontrará?")

st.write("✅ Estatísticas descritivas sobre os dados")
st.write("✅ Comparação de indicadores entre países")
st.write("✅ Análises gráficas e interativas")
st.write("✅ Distribuição de doenças e seu impacto na expectativa de vida")

st.subheader("Conclusões e Insights")

st.write("A análise dos dados de expectativa de vida nos permite tirar diversas conclusões sobre os fatores que impactam diretamente a longevidade das populações.")

st.write("- Países desenvolvidos apresentam, em geral, uma expectativa de vida significativamente maior do que países em desenvolvimento. Isso pode estar ligado a melhores condições de saneamento, acesso à saúde e padrões de vida mais elevados.")

st.write("- Vacinas como Hepatite B, Poliomielite e Difteria mostram uma forte correlação com o aumento da expectativa de vida. Regiões com baixa cobertura vacinal tendem a apresentar maior mortalidade infantil e menor longevidade.")

st.subheader("💡 Conclusão Final")

st.write("A expectativa de vida é um reflexo de múltiplos fatores, como acesso à saúde, educação, vacinação e condições socioeconômicas. Melhorar esses indicadores pode ter um impacto significativo na longevidade e qualidade de vida das populações.")