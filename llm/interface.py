import streamlit as st
from streamlit_chat import message
from llm.langchain_setup import LangChainClient
from llm.openai_setup import OpenAIClient

langchain_client = LangChainClient()
openai_client = OpenAIClient()
pre_response = openai_client.get_response_from_gpt(prompt_template=langchain_client.prompt_templates())

def on_input_change():
    user_input = st.session_state.user_input
    response_text = langchain_client.get_response_from_gpt(query_text=user_input, response_gpt=pre_response)
    st.session_state.past.append(user_input)
    st.session_state.generated.append({"type": "normal", "data": response_text})

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

st.title("Chat com assistente logístico - Albert Einstein")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i].get('type') == 'table' else False
        )
    
    st.button("Limpar histórico", on_click=on_btn_click)

with st.container():
    st.text_input("Mensagem:", on_change=on_input_change, key="user_input")
