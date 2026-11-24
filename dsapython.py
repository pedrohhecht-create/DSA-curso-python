# Estudo de Caso 1 - DSA AI Coder - Criando Seu Assistente de Programação Python, em Python

import os
import streamlit as st
from groq import Groq

# Configura a página do Streamlit
st.set_page_config(
    page_title="DSA AI Coder",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define o prompt de sistema (suas regras)
CUSTOM_PROMPT = """
Você é o "DSA Coder", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas.

REGRAS DE OPERAÇÃO:
1. **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário fugir do tema, avise.
2. **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
   * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
   * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
   * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
   * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial.
3. **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# ==========================================
# CÓDIGO EXATO DA IMAGEM DO PROFESSOR (BARRA LATERAL)
# ==========================================
with st.sidebar:
    st.title("🤖 DSA AI Coder")
    st.markdown("Um assistente de IA focado em programação Python para ajudar iniciantes.")
    
    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )
    
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em suas dúvidas de programação com Linguagem Python. IA pode cometer erros. Sempre verifique as respostas.")
    st.markdown("---")
    st.markdown("Conheça os Cursos Individuais, Formações e Programas de Pós-Graduação da DSA:")
    st.markdown("[Data Science Academy](https://www.datascienceacademy.com.br/)")

# ==========================================
# PARTE DO CHAT (O que o vídeo não mostrou ainda)
# ==========================================
st.title("Data Science Academy - DSA AI Coder")
st.subheader("Assistente Pessoal de Programação Python 🐍")
st.caption("Faça sua pergunta sobre a Linguagem Python e obtenha código, explicações e referências.")

# Se a chave não foi digitada na barra lateral, o site para aqui.
if not groq_api_key:
    st.info("👈 Por favor, insira sua API Key da Groq na barra lateral para começar.")
    st.stop()

# Se a chave foi digitada, conecta com a Groq
client = Groq(api_key=groq_api_key)

# Histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de pergunta
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                mensagens_api = [{"role": "system", "content": CUSTOM_PROMPT}]
                for m in st.session_state.messages:
                    mensagens_api.append({"role": m["role"], "content": m["content"]})

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=mensagens_api,
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Erro: {e}")
