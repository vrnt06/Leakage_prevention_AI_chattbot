# chatbot_engine.py
import google.generativeai as genai

# System instructions forcing the AI to maintain its SDG infrastructure alignment persona
SDG_6_SYSTEM_PROMPT = (
    "You are an AI Utility Logistics Specialist dedicated to UN SDG 6: Clean Water and Sanitation. "
    "Your core task is to handle citizen reports regarding water pipe bursts, leaks, or pollution. "
    "Ask clarifying questions to determine the location, flow rate (e.g., dripping vs. gushing), and duration of the problem. "
    "Be highly professional and direct. Always conclude every response with a hidden logistics classification string "
    "on a brand new line at the very bottom, formatted exactly like this: "
    "[SEVERITY: CRITICAL], [SEVERITY: MODERATE], or [SEVERITY: MINOR]."
)

def initialize_water_bot(api_key):
    """Initializes a fresh, structured conversational session with Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SDG_6_SYSTEM_PROMPT
    )
    return model.start_chat(history=[])

def evaluate_leakage_metrics(ai_reply_text):
    """Parses structural severity strings to dynamically adjust water waste indexes."""
    if "[SEVERITY: CRITICAL]" in ai_reply_text:
        return 1200, "Critical Burst (Immediate Dispatch Required) 🚨"
    elif "[SEVERITY: MODERATE]" in ai_reply_text:
        return 250, "Moderate Leakage (Schedule Within 24 Hours) ⚠️"
    else:
        return 15, "Minor Seepage (Routine Maintenance Task) 🔄"
