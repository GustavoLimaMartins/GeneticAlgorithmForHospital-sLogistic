from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(SCRIPT_DIR, "chroma")
DATA_PATH = os.path.join(SCRIPT_DIR, "logistic_infos_docs")

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documentos()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documentos():
    # Carregar arquivos Markdown (.md)
    loader = DirectoryLoader(
        DATA_PATH, 
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {DATA_PATH}")
    return docs

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=450,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
    