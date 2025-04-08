from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class ReadFile:
    @classmethod
    def load_pdf(cls, pdf_file: str):
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        return documents

class FullSummarize():
    @classmethod
    def full_summarize(cls, documents: list) -> str:
        model = ChatGroq(temperature=0.1, model_name="llama-3.3-70b-versatile")
        chain = load_summarize_chain(model, chain_type="stuff")
        result = chain.invoke({"input_documents":documents})
        return result['output_text']

class UserRangeSummarize():
    @classmethod
    def range_summarize(cls, documents: list, start_user_page = 0, end_user_page = 2) -> str:
        model = ChatGroq(temperature=0.1, model_name="llama-3.3-70b-versatile")
        for i in range(start_user_page, end_user_page):
            chain = load_summarize_chain(model, chain_type='stuff')
            result = chain.invoke({"input_documents": [documents[i]]})['output_text']
        return result

class Retriever():
    @classmethod
    def retrieve(cls, documents: list):
        chunk = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = False)
        split_pdf = chunk.split_documents(documents)
        db = FAISS.from_documents(documents=split_pdf, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
        return db 
    
class Questions_and_Answers():
    @classmethod
    def qa_chain(cls,database, user_question: str) -> str:
        retriever = database.as_retriever(search_type="similarity")
        system_prompt = (
            "You are a PDF Reader Assistant."
            "Provide very concisly and professional responses Must be 2000 or fewer in length."
            "If the user asks a part of PDF, give clear and helpful information about it."
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate(
            [
                ("system",system_prompt),
                ("human", "{input}"),
            ]
            )
        
        try:
            groq_model = ChatGroq(
                temperature=0.1,
                model_name="llama-3.3-70b-versatile"
            )
            stuff_chain = create_stuff_documents_chain(groq_model, prompt)
            output = create_retrieval_chain(retriever, stuff_chain)
            answer_output = output.invoke({"input": user_question})['answer']
            return answer_output
        
        except Exception as e:
            
            gemini_model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key="AIzaSyCTWU4EWjxo3LjnPZZvC0dPMX098tkSOP0",
                temperature=0.2,
                max_tokens=None
            )
            stuff_chain = create_stuff_documents_chain(gemini_model, prompt)
            output = create_retrieval_chain(retriever, stuff_chain)
            answer_output = output.invoke({"input": user_question})['answer']
            return answer_output
