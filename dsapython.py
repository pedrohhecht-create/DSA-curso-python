import streamlit as st
from groq import Groq

st.set_page_config(page_title="DSA AI Coder", page_icon="🐍")
st.title("🤖 Assistente Pessoal de Programação Python")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Chave de API não configurada. Vá em Settings > Secrets no Streamlit.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Erro: {e}")
