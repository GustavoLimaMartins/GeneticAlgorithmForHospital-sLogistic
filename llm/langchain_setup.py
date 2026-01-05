from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import random

class LangChainClient:
    def __init__(self, persist_directory: str = "chroma_db"):
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings()
        )

    def prompt_templates(self, context: str, question: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            """
            Responda como um assistente especialista em logística e roteirização de veículos.
            Forneça respostas detalhadas e técnicas, utilizando terminologia específica do setor.
            Utilize exemplos práticos e estudos de caso para ilustrar conceitos complexos.
            Mantenha um tom profissional e objetivo, focando na clareza e precisão das informações:
            
            {context}
            
            ----------------------------------------------------------------------------------------
           
            Pergunta: {question}
            """
        )
    
        return prompt.format(context=context, question=question)
    
    def get_response_from_gpt(self, query_text: str, response_gpt: function) -> str:
        results = self.vector_store.similarity_search(query_text, k=4)
        if len(results) == 0 or results[0][1] < 0.7:
            return "Não foi possível encontrar resultados correspondentes.", []

        random.shuffle(results)
        context = "\n\n".join([doc.page_content for doc, _ in results])
        prompt_rag = self.prompt_templates(context, query_text)
        response_text = response_gpt(prompt_rag)
        
        response_with_sources = f"{response_text}\n\nFontes:\n"
        return response_with_sources
