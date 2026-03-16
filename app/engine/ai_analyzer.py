# app/engine/ai_analyzer.py
import os
import json
import google.generativeai as genai
from app.schemas import RfpAnalysis

# Fetch the API key from the environment variables (GitHub Secrets)
# We use os.getenv and raise a clear ValueError if it's missing.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=api_key)

# The persona and main directive for the AI
SYSTEM_INSTRUCTION = (
    "You are a procurement expert and CTO. "
    "Your task is to ruthlessly analyze the document and identify hidden traps."
)

async def analyze_rfp_text(cleaned_text: str) -> RfpAnalysis:
    """
    Sends the pre-processed RFP text to Gemini 1.5 Pro and returns a structured Pydantic object.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2, 
        )
    )

    schema_blueprint = RfpAnalysis.model_json_schema()
    
    prompt = (
        f"Analyze the following RFP document text and extract the critical information.\n"
        f"You MUST return a valid JSON object that strictly adheres to the following JSON Schema:\n"
        f"{json.dumps(schema_blueprint, indent=2)}\n\n"
        f"--- RFP DOCUMENT TEXT ---\n"
        f"{cleaned_text}\n"
        f"-------------------------"
    )

    response = await model.generate_content_async(prompt)
    
    # Parse and validate through Pydantic
    raw_json = json.loads(response.text)
    validated_analysis = RfpAnalysis(**raw_json)
    
    return validated_analysis