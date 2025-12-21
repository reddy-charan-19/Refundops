import google.generativeai as genai
import json

# --- PASTE YOUR GOOGLE API KEY HERE ---
GOOGLE_API_KEY = "AIzaSyDhnvlksy3gth7einKjs6AV1pKIgTFqRFQ"

genai.configure(api_key=GOOGLE_API_KEY)
        # Using Gemini 2.0 Flash (Free & Fast)
model = genai.GenerativeModel(
    'models/gemini-2.0-flash-lite',
    generation_config={"response_mime_type": "application/json"}
)

def get_flight_data(email_text):
    print("🧠 BRAIN: Reading email...", flush=True)
    
    # Prompt specifically asks for the Airline Name now
    prompt = f"""
    You are a data extraction agent.
    Extract the following details from this email. Return ONLY a single JSON object (not an array).
    
    Required format (must be an object, not an array):
    {{
        "pnr": "ABC123",
        "airline": "Air India"
    }}
    
    Fields to extract:
    - pnr (string) -> The booking reference (usually 6 chars)
    - airline (string) -> Example: "Indigo", "Air India", "Vistara"
    
    Email Text:
    "{email_text}"
    
    Return ONLY the JSON object, nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        
        # If result is a list, take the first item
        if isinstance(result, list):
            result = result[0] if len(result) > 0 else None
            
        return result
    except Exception as e:
        print(f"❌ Brain Error: {e}")
        return None