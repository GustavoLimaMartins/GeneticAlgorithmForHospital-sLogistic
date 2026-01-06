import streamlit as st
from streamlit_chat import message
from langchain_setup import LangChainClient
from openai_setup import OpenAIClient
import json
import os

class StreamlitInterface:
    def __init__(self, solutions_metadata: str = None):
        self.langchain_client = LangChainClient()
        self.openai_client = OpenAIClient()
        
        # Load solutions from JSON file if not provided
        if solutions_metadata is None:
            solutions_file = 'solutions_data.json'
            if os.path.exists(solutions_file):
                with open(solutions_file, 'r', encoding='utf-8') as f:
                    solutions_data = json.load(f)
                self.solutions_metadata = json.dumps(solutions_data['best_solutions'], indent=4)
            else:
                self.solutions_metadata = json.dumps({
                    "message": "No solutions available. Run the genetic algorithm first."
                })
        else:
            self.solutions_metadata = solutions_metadata

    def on_input_change(self):
        user_input = st.session_state.user_input
        response_text = self.langchain_client.get_response_from_gpt(
            query_text=user_input,
            openai_client=self.openai_client,
            solutions_metadata=self.solutions_metadata
        )
        st.session_state.past.append(user_input)
        st.session_state.generated.append({"type": "normal", "data": response_text})

    def on_btn_click(self):
        del st.session_state.past[:]
        del st.session_state.generated[:]

    def run(self):
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
            
            st.button("Limpar histórico", on_click=self.on_btn_click)

        with st.container():
            st.text_input("Mensagem:", on_change=self.on_input_change, key="user_input")

if __name__ == "__main__":
    interface = StreamlitInterface()
    interface.run()
    #python -m streamlit run "agent-llm.py"