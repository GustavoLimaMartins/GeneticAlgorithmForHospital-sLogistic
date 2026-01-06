from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

class LangChainClient:
    def __init__(self, persist_directory: str = "chroma"):
        # Verificar se a chave da API está configurada
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY não encontrada. "
                "Crie um arquivo .env na raiz do projeto com: OPENAI_API_KEY=sua_chave_aqui"
            )
        
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings()
        )

    def prompt_templates(self, context: str, question: str, solutions_metadata: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            """
            Responda como um assistente especialista em logística e roteirização de veículos.
            Seja objetivo e direto ao ponto, como numa conversa profissional.
            Use as informações fornecidas no contexto para fundamentar suas respostas, não especule.
            Não elocubre além do que está no contexto e nas soluções fornecidas.
            Quando solicitada sugestões de melhorias, baseie-se no contexto fornecido.
            Mantenha um tom profissional e objetivo, focando na clareza e precisão das informações do contexto:
            
            {context}
            
            ----------------------------------------------------------------------------------------
            Soluções do algoritmo genético para roteirização de veículos encontradas no banco de dados, use as informações abaixo para fundamentar suas respostas:
            
            {solutions_metadata}
            
            ----------------------------------------------------------------------------------------

            Pergunta: {question}
            """
        )
    
        return prompt.format(context=context, question=question, solutions_metadata=solutions_metadata)
    
    def get_response_from_gpt(self, query_text: str, openai_client, solutions_metadata: dict = None) -> str:
        # Find similar documents from the vector store
        results = self.vector_store.similarity_search_with_score(query_text, k=4)
        
        if len(results) == 0:
            return "Não foi possível encontrar resultados correspondentes."
        
        # Extract context from the retrieved documents
        context = "\n\n".join([doc.page_content for doc, _ in results])
        
        # Create prompt with context
        prompt_rag = self.prompt_templates(context, query_text, solutions_metadata)
        
        # Get response from GPT
        response_text = openai_client.get_response_from_gpt(prompt_template=prompt_rag)
        
        # Add sources
        sources = "\n".join([f"- {doc.metadata.get('source', 'Unknown')}" for doc, _ in results])
        response_with_sources = f"{response_text}\n\n**Sources:**\n{sources}"
        
        return response_with_sources
