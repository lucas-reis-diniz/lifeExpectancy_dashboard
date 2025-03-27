import streamlit as st
import pandas as pd
import openai
import os
import time
from dotenv import load_dotenv

# 🔥 Carregar Variáveis de Ambiente
api_key = st.secrets["OPENAI_API_KEY"]

# Configuração do OpenAI para OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Inicializa histórico de mensagens no session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Função para IA responder perguntas
def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro na API: {str(e)}"


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


# Carregar os dados (opcional)
@st.cache_data
def load_data():
    return pd.read_csv("LifeExpectancy.csv")


df = load_data()
