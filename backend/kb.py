from typing import Dict

KNOWLEDGE_BASE: Dict[str, Dict[str, str]] = {
    "api_config": {
        "technical_expert": "To configure the API, set the BASE_URL in your .env file and ensure the AUTH_TOKEN is valid. The endpoint expects JSON payloads.",
        "frustrated_user": "I'm sorry you're having trouble with the API. Let's get it set up correctly. You just need to add your secret key to the settings.",
        "business_executive": "Our API integration is designed for seamless enterprise connectivity, ensuring maximum ROI through automated data flows.",
        "general_user": "You can configure the API by following the steps in the settings menu."
    },
    "billing_issue": {
        "technical_expert": "Billing cycles are processed via a cron job every 30 days. Transaction logs are available in the dashboard.",
        "frustrated_user": "I understand the billing concern is upsetting. I'm checking your account right now to fix any errors.",
        "business_executive": "Our billing system is optimized for transparent cost management and predictable enterprise budgeting.",
        "general_user": "You can view your billing history in the account section."
    },
    "system_down": {
        "technical_expert": "The system is experiencing a 503 Service Unavailable error due to a database connection pool exhaustion.",
        "frustrated_user": "I am so sorry the system is down. We are working as fast as possible to bring it back online for you.",
        "business_executive": "We are currently addressing a temporary service interruption to maintain our 99.9% uptime commitment.",
        "general_user": "The system is currently undergoing maintenance. Please try again later."
    },
    "resume_help": {
        "technical_expert": "For a technical resume, focus on your stack, GitHub contributions, and specific project architectures you've designed.",
        "frustrated_user": "I hear you're looking to build a resume. Let's make this process as stress-free as possible for you.",
        "business_executive": "A strong executive resume should highlight leadership, strategic impact, and measurable business growth.",
        "general_user": "I can help you build a resume! Start by listing your work experience and key skills."
    },
    "general_help": {
        "technical_expert": "I'm ready to assist with technical queries, API integrations, or system architecture discussions.",
        "frustrated_user": "I'm here for you. Please let me know what's on your mind, and I'll do my best to help you through it.",
        "business_executive": "I can provide insights on system value, operational efficiency, and strategic alignment.",
        "general_user": "I'm here to help! What would you like to talk about or work on today?"
    }
}

def get_kb_content(query: str, persona: str) -> str:
    # Simple keyword matching for KB retrieval
    query = query.lower()
    if "api" in query or "config" in query:
        key = "api_config"
    elif "bill" in query or "pay" in query:
        key = "billing_issue"
    elif "down" in query or "not working" in query or "error" in query:
        key = "system_down"
    elif "resume" in query or "cv" in query:
        key = "resume_help"
    else:
        key = "general_help"
    
    return KNOWLEDGE_BASE[key].get(persona, KNOWLEDGE_BASE[key]["general_user"])
