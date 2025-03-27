import streamlit as st
import pandas as pd
import openai
import os
import time

api_key = st.secrets.get("OPENROUTER_API_KEY", None)

if not api_key:
    st.error("❌ Erro: Chave da API não encontrada! Configure-a no Streamlit Secrets.")

# Configuração do OpenAI para OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Função para carregar os dados
@st.cache_data
def load_data():
    return pd.read_csv("LifeExpectancy.csv")

df = load_data()

# Inicializa histórico de mensagens no session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Função para processar a pergunta e buscar resposta nos dados
def get_data_response(question):
    question_lower = question.lower()

    # Exemplo: verificar se a pergunta contém palavras-chave
    if "expectativa de vida média" in question_lower:
        avg_life_expectancy = df["Life expectancy"].mean()
        return f"A expectativa de vida média global no dataset é **{avg_life_expectancy:.2f} anos**."

    elif "expectativa de vida no" in question_lower or "expectativa de vida em" in question_lower:
        for country in df["Country"].unique():
            if country.lower() in question_lower:
                country_life_expectancy = df[df["Country"] == country]["Life expectancy"].mean()
                return f"A expectativa de vida média em **{country}** é **{country_life_expectancy:.2f} anos**."

    elif "país com maior expectativa de vida" in question_lower:
        max_country = df.loc[df["Life expectancy"].idxmax()]["Country"]
        max_life = df["Life expectancy"].max()
        return f"O país com **maior expectativa de vida** é **{max_country}**, com **{max_life:.2f} anos**."

    elif "país com menor expectativa de vida" in question_lower:
        min_country = df.loc[df["Life expectancy"].idxmin()]["Country"]
        min_life = df["Life expectancy"].min()
        return f"O país com **menor expectativa de vida** é **{min_country}**, com **{min_life:.2f} anos**."

    elif "relação entre pib e expectativa de vida" in question_lower:
        correlation = df["GDP"].corr(df["Life expectancy"])
        return f"A correlação entre **PIB** e **expectativa de vida** no dataset é **{correlation:.2f}**, indicando uma relação {'positiva' if correlation > 0 else 'negativa'}."

    else:
        return None  # Se não encontrar nada no dataset, passa para a IA


# Função para IA responder perguntas
def ask_ai(question):
    # Primeiro, tenta buscar nos dados
    data_response = get_data_response(question)
    if data_response:
        return data_response  # Se encontrar resposta nos dados, retorna imediatamente

    # Se não houver resposta nos dados, chama a IA
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro na API: {str(e)}"


# Interface do Chatbot
st.title("🤖 Chatbot de Expectativa de Vida")

for message in st.session_state["messages"]:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

question = st.chat_input("Digite sua pergunta...")

if question:
    # Exibir mensagem do usuário
    st.session_state["messages"].append({"role": "user", "avatar": "👤", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # Criar espaço para animação de "digitando..."
    with st.chat_message("assistant", avatar="🤖"):
        typing_placeholder = st.empty()

        # Animação de "digitando..." 🤖💬
        for dots in ["", ".", "..", "..."]:
            typing_placeholder.markdown(f"🤖 Digitando{dots}")
            time.sleep(0.5)  # Aguarda meio segundo entre os passos

        response = ask_ai(question)
        typing_placeholder.markdown(response)

    # Salvar resposta no histórico
    st.session_state["messages"].append({"role": "assistant", "avatar": "🤖", "content": response})
