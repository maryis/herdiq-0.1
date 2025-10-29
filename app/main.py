from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import Agent

app = FastAPI(title="Agentic AI (DB + Web + Cached Context)")
agent = Agent()

class Query(BaseModel):
    user_input: str

@app.post("/query")
async def query_agent(q: Query):
    response = await agent.run(q.user_input)
    return {"response": response}
