from enum import Enum
from typing import Dict, List

class Persona(str, Enum):
    TECHNICAL = "technical_expert"
    FRUSTRATED = "frustrated_user"
    EXECUTIVE = "business_executive"
    GENERAL = "general_user"

def detect_persona(text: str) -> Persona:
    text = text.lower()
    
    # Technical Expert keywords
    tech_keywords = ["api", "endpoint", "configuration", "debug", "logs", "stack", "implementation", "latency", "deployment"]
    if any(word in text for word in tech_keywords):
        return Persona.TECHNICAL
    
    # Frustrated User keywords/patterns
    frustrated_keywords = ["not working", "broken", "useless", "third time", "fix this", "terrible", "worst", "angry"]
    if any(word in text for word in frustrated_keywords) or text.count("!") > 2 or text.isupper():
        return Persona.FRUSTRATED
    
    # Business Executive keywords
    exec_keywords = ["roi", "cost", "efficiency", "enterprise", "strategy", "value", "bottom line", "quarterly", "growth"]
    if any(word in text for word in exec_keywords):
        return Persona.EXECUTIVE
    
    return Persona.GENERAL

def adapt_response(content: str, persona: Persona) -> str:
    if persona == Persona.TECHNICAL:
        return f"Technical Analysis: {content}\n\nTechnical Details: The underlying system is operating within expected parameters. You can verify this via the /health endpoint."
    elif persona == Persona.FRUSTRATED:
        return f"I sincerely apologize for the frustration this has caused. I understand how important this is for you. {content}\n\nI am prioritizing your request and will ensure we get this resolved immediately."
    elif persona == Persona.EXECUTIVE:
        return f"Strategic Overview: {content}\n\nValue Proposition: This solution optimizes operational efficiency and ensures long-term scalability for the enterprise."
    else:
        return f"Support Assistant: {content}\n\nIs there anything else I can help you with?"
