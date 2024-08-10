from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


class QnAChatBot:
    def __init__(self, pdf_path:str, db_path:str, chain_type:str="stuff") -> None:
        print(f"Env Variables are loaded: {load_dotenv()}")
        self.docs = []
        self.db = None
        self.retriever = None
        self.model = ChatOpenAI()
        self.chain = None
        self.load_pdfs(pdf_path)
        self.build_db(db_path)
        self.build_retriever()
        self.build_chain(chain_type)

    def load_pdfs(self, dir_path:str) -> None:
        for f_name in os.listdir(dir_path):
            if f_name.endswith(".pdf"):
                print(f"System: {f_name} loaded")
                f_path = os.path.join(dir_path, f_name)
                loader = PDFMinerLoader(f_path)
                docs = loader.load()
                self.docs.extend(docs)
        print(f"System: {len(self.docs)} documents have benn loaded in total.")
        
    def build_db(self, persist_dir:str) -> None: 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(self.docs)

        # Making Database
        embedding = OpenAIEmbeddings() # embedding function

        if os.path.exists(persist_dir):
            print("System: Database already exists. Loading the existing DB...")
            self.db = Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding)
        else:
            print("System: Creating a new database...")
            self.db = Chroma.from_documents(
                documents=texts,
                embedding=embedding,
                persist_directory=persist_dir)
            self.db.persist() # save the current state of vector db to disk (reload w/o recomputing the embeddings)
        
    def build_retriever(self) -> None:
        if self.db is None:
            print("System: Database does not exist. Create DB first.")
            return
        self.retriever = self.db.as_retriever()
        print("System: Retriever has been built successfully")
        
    def build_chain(self, chain_type:str) -> None:
        self.chain = RetrievalQA.from_chain_type(
                                llm=self.model,
                                chain_type=chain_type,
                                retriever=self.retriever,
                                return_source_documents=True)

    def process_llm_response(self, llm_response:dict) -> dict:
        answer = dict()
        answer['content'] = llm_response['result']
        answer['source'] = []
        for source in llm_response["source_documents"]:
            answer['source'].append("".join(source.metadata['source']))
        return answer

    def query(self, question:str) -> dict:
        llm_response = self.chain(question)
        answer = self.process_llm_response(llm_response)
        return answer


# query = "음식물이 묻은 비닐 쓰레기는 어떻게 배출해야 돼?"
# llm_response = qa_chain(query)
# answer = process_llm_response(llm_response)
# print(answer)

# query = "테이프가 붙은 종이박스는 어떻게 배출해야 돼?"
# llm_response = qa_chain(query)
# answer = process_llm_response(llm_response)
# print(answer)

# query = "테슬라 배터리는 어떻게 버려야 돼?"
# llm_response = qa_chain(query)
# answer = process_llm_response(llm_response)
# print(answer)