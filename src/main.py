from fastapi import FastAPI, UploadFile, File, Form
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
import os
import shutil
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

def load_pdf_from_file_path(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=False)
    split_docs = splitter.split_documents(documents)
    return split_docs

@app.post("/full_summarize")
async def full_summarize(file: UploadFile = File(...)):
    # Save uploaded file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    split_pdf = load_pdf_from_file_path(temp_path)
    model = ChatGroq(temperature=0.1, model_name="llama-3.1-8b-instant")
    chain = load_summarize_chain(model, chain_type="stuff")
    result = chain.invoke(split_pdf)['output_text']

    os.remove(temp_path)  # Clean up
    return {"summary": result}

@app.post("/range_summarize")
async def range_summarize(file: UploadFile = File(...), user_input: int = Form(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    split_pdf = load_pdf_from_file_path(temp_path)
    model = ChatGroq(temperature=0.1, model_name="llama-3.1-8b-instant")
    results = []
    for i in range(min(user_input, len(split_pdf))):
        chain = load_summarize_chain(model, chain_type='stuff')
        result = chain.invoke({"input_documents": [split_pdf[i]]})['output_text']
        results.append(result)

    os.remove(temp_path)
    return {"summaries": results}

# Test Case

### non_user_input: full_summarize = full_summarize(r"D:\Programming\Summarize PDF\IRT_Machine_Translation.pdf")
### print("Full Summarize: ", non_user_input)

### yes_user_input: range_summarize = range_summarize(r"D:\Programming\Summarize PDF\IRT_Machine_Translation.pdf",2)
### print("User input range Summarize: ",yes_user_input)

