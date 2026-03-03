from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from persona import detect_persona, adapt_response
from kb import get_kb_content
from escalation import should_escalate, get_escalation_context

app = FastAPI(title="Persona-Adaptive Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    persona: str
    escalated: bool
    context: Optional[dict] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    persona = detect_persona(request.message)
    kb_content = get_kb_content(request.message, persona)
    response_text = adapt_response(kb_content, persona)
    
    escalated = should_escalate(request.message, persona)
    context = None
    if escalated:
        context = get_escalation_context(request.history + [{"query": request.message, "persona": persona}])
        response_text = "I am escalating this to a human agent who can better assist you. They will have all the context of our conversation."

    return ChatResponse(
        response=response_text,
        persona=persona,
        escalated=escalated,
        context=context
    )

@app.get("/")
async def root():
    return {"message": "Persona-Adaptive Support Agent API is running"}
