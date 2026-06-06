# chatbot_engine.py
from google import genai
from google.genai import types

SDG_6_SYSTEM_PROMPT = (
    "You are an AI Utility Logistics Specialist dedicated to UN SDG 6: Clean Water and Sanitation. "
    "Your core task is to handle citizen reports regarding water pipe bursts, leaks, or pollution. "
    "Ask clarifying questions to determine the location, flow rate (e.g., dripping vs. gushing), and duration of the problem. "
    "Be highly professional and direct. Always conclude every response with a hidden logistics classification string "
    "on a brand new line at the very bottom, formatted exactly like this: "
    "[SEVERITY: CRITICAL], [SEVERITY: MODERATE], or [SEVERITY: MINOR]."
)

def initialize_water_bot(api_key):
    """Initializes the modern Google Gen AI Client."""
    # Instantiates the current production SDK Client layer
    return genai.Client(api_key=api_key)

def send_ai_message(client, user_message, chat_history):
    """Handles chat context using the standard system instructions template configuration."""
    # Convert our local tracking history back into the explicit type objects expected by the SDK
    formatted_contents = []
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(types.Content(
            role=role,
            parts=[types.Part.from_text(text=msg["content"])]
        ))
    
    # Append the newest user input frame
    formatted_contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)]
    ))

    # Send using the current generation production standard models
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=formatted_contents,
        config=types.GenerateContentConfig(
            system_instruction=SDG_6_SYSTEM_PROMPT,
            temperature=0.7
        )
    )
    return response.text

def evaluate_leakage_metrics(ai_reply_text):
    """Parses structural severity strings to dynamically adjust water waste indexes."""
    if "[SEVERITY: CRITICAL]" in ai_reply_text:
        return 1200, "Critical Burst (Immediate Dispatch Required) 🚨"
    elif "[SEVERITY: MODERATE]" in ai_reply_text:
        return 250, "Moderate Leakage (Schedule Within 24 Hours) ⚠️"
    else:
        return 15, "Minor Seepage (Routine Maintenance Task) 🔄"
