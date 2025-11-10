from fastapi import FastAPI, Query
import os
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

app = FastAPI()

CHROMA_URL = os.getenv("CHROMA_URL", "http://chroma:8000")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/agent/ask")
async def ask_agent(query: str = Query(...)):
    try:
        llm = OpenAI(openai_api_key=OPENAI_KEY, temperature=0.7)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
        db = Chroma(collection_name="test", embedding_function=embeddings, persist_directory="/chroma/chroma")
        docs = db.similarity_search(query)
        response = llm(f"User asked: {query}. Related docs: {docs}")
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/agent/health")
def health():
    return {"status": "Agent running"}
