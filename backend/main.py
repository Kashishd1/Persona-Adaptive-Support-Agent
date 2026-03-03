import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from persona import detect_persona, adapt_response
from kb import get_kb_content
from escalation import should_escalate, get_escalation_context


# -------------------------------
# App Initialization
# -------------------------------

app = FastAPI(title="Persona-Adaptive Support Agent")

# -------------------------------
# Logging Setup
# -------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# CORS Configuration (Production Safe)
# -------------------------------

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "https://persona-adaptive-support-agent.vercel.app"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# -------------------------------
# Request / Response Models
# -------------------------------

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    response: str
    persona: str
    escalated: bool
    context: Optional[Dict[str, Any]] = None


# -------------------------------
# Chat Endpoint
# -------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Incoming message: {request.message}")

        # Detect persona
        persona = detect_persona(request.message)

        # Retrieve KB content
        kb_content = get_kb_content(request.message, persona)

        # Adapt tone
        response_text = adapt_response(kb_content, persona)

        # Escalation logic
        escalated = should_escalate(request.message, persona)
        context = None

        if escalated:
            context = get_escalation_context(
                request.history + [{
                    "query": request.message,
                    "persona": persona
                }]
            )
            response_text = (
                "I am escalating this to a human agent who can better assist you. "
                "They will have full context of our conversation."
            )

        return ChatResponse(
            response=response_text,
            persona=persona,
            escalated=escalated,
            context=context
        )

    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


# -------------------------------
# Health Check Endpoint
# -------------------------------

@app.get("/")
async def root():
    return {"message": "Persona-Adaptive Support Agent API is running"}