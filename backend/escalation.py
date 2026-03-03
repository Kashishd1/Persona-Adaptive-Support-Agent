from typing import Dict, Optional

def should_escalate(text: str, persona: str) -> bool:
    text = text.lower()
    # Escalate if frustrated user remains angry or explicitly asks for a human
    escalation_triggers = ["human", "person", "manager", "supervisor", "speak to someone", "real agent"]
    
    if any(trigger in text for trigger in escalation_triggers):
        return True
    
    if persona == "frustrated_user" and ("still not working" in text or "unacceptable" in text):
        return True
        
    return False

def get_escalation_context(history: list) -> Dict:
    return {
        "summary": "User is experiencing persistent issues and requires human intervention.",
        "persona_detected": history[-1].get("persona") if history else "Unknown",
        "last_query": history[-1].get("query") if history else "N/A",
        "interaction_count": len(history)
    }
