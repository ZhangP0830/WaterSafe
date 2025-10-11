from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/api/symptoms", tags=["symptoms"])

# Initialize OpenAI client conditionally
client = None
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")
    print(f"OpenAI API Key found: {'Yes' if api_key and api_key != 'sk-test-key-for-development' else 'No'}")
    print(f"OpenAI Model: {model}")
    if api_key and api_key != "sk-test-key-for-development" and api_key != "your_openai_api_key_here" and api_key.strip():
        # Set the API key as environment variable for OpenAI to pick up
        os.environ["OPENAI_API_KEY"] = api_key.strip()
        # Initialize client without any extra parameters
        client = OpenAI()
        print("OpenAI client initialized successfully")
    else:
        print("OpenAI client not initialized - using development mode")
except Exception as e:
    print(f"OpenAI client initialization failed: {e}")
    print("Falling back to development mode")
    client = None

class SymptomAssessmentRequest(BaseModel):
    subject: str  # "pregnant" or "infant"
    chips: List[str]
    freeText: str
    severityHints: str  # "mild|moderate|severe|unknown"
    context: Dict[str, str]

class SymptomAssessmentResponse(BaseModel):
    classification: str  # "self_care|seek_care|urgent"
    reason: str
    steps: List[str]
    watch_for: List[str]
    references: List[Dict[str, str]]
    disclaimer: str

# System prompt for the LLM
SYSTEM_PROMPT = """You are a helpful medical assistant providing guidance for pregnant women and infant caregivers during water safety disruptions. 

IMPORTANT RULES:
1. Speak calmly and use grade-6 reading level language
2. Never diagnose or provide medical advice - only suggest next steps
3. Classify symptoms as: self_care, seek_care, or urgent
4. For urgent/red flag symptoms, always recommend calling emergency services
5. Provide 3-6 clear, actionable next steps
6. Include watch-for signs and explain why (briefly)
7. Add trusted references (WHO, CDC, local health) with URLs
8. Always include a disclaimer about not replacing professional medical advice

For pregnant women, be especially cautious about:
- Severe abdominal pain, bleeding, contractions
- High fever, severe dehydration
- Difficulty breathing, chest pain
- Severe headaches, vision changes

For infants, be especially cautious about:
- High fever, difficulty breathing
- Severe dehydration, lethargy
- Feeding refusal, unusual crying
- Any signs of distress

Respond in valid JSON format only."""

@router.post("/assess", response_model=SymptomAssessmentResponse)
async def assess_symptoms(request: SymptomAssessmentRequest):
    """
    Assess symptoms and provide safe next steps using LLM
    """
    try:
        # Check if OpenAI client is available
        if client is None:
            # Return mock response for development
            return SymptomAssessmentResponse(
                classification="seek_care",
                reason="Development mode - please configure OpenAI API key for full functionality",
                steps=[
                    "Contact your healthcare provider",
                    "Monitor symptoms closely",
                    "Seek emergency care if symptoms worsen",
                    "Keep a record of symptoms and their timing"
                ],
                watch_for=[
                    "Severe pain or discomfort",
                    "High fever",
                    "Difficulty breathing",
                    "Signs of severe dehydration"
                ],
                references=[
                    {"label": "Local Health", "url": "https://www.health.gov.au/"},
                    {"label": "WHO", "url": "https://www.who.int/"}
                ],
                disclaimer="This is not a substitute for professional medical advice. Always consult healthcare providers for medical concerns."
            )
        # Prepare the user prompt
        symptoms_text = ""
        if request.chips:
            symptoms_text += f"Selected symptoms: {', '.join(request.chips)}\n"
        if request.freeText.strip():
            symptoms_text += f"Additional symptoms: {request.freeText}\n"
        
        severity_text = f"Severity: {request.severityHints}\n" if request.severityHints != "unknown" else ""
        context_text = f"Context: {request.context.get('mode', 'general')} situation, at {request.context.get('place', 'home')}\n"
        
        user_prompt = f"""Subject: {request.subject}
{symptoms_text}{severity_text}{context_text}

Please assess these symptoms and provide guidance in the following JSON format:
{{
    "classification": "self_care|seek_care|urgent",
    "reason": "Brief explanation of why this classification",
    "steps": ["Step 1", "Step 2", "Step 3"],
    "watch_for": ["Warning sign 1", "Warning sign 2"],
    "references": [{{"label": "WHO", "url": "https://..."}}, {{"label": "CDC", "url": "https://..."}}],
    "disclaimer": "This is not a substitute for professional medical advice. Always consult healthcare providers for medical concerns."
}}"""

        # Call OpenAI API
        try:
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
        except Exception as api_error:
            print(f"OpenAI API call failed: {api_error}")
            # Return fallback response
            return SymptomAssessmentResponse(
                classification="seek_care",
                reason="Unable to process symptoms. Please seek medical advice.",
                steps=[
                    "Contact your healthcare provider immediately",
                    "Monitor symptoms closely",
                    "Seek emergency care if symptoms worsen",
                    "Keep a record of symptoms and their timing"
                ],
                watch_for=[
                    "Severe pain or discomfort",
                    "High fever",
                    "Difficulty breathing",
                    "Signs of severe dehydration"
                ],
                references=[
                    {"label": "Local Health", "url": "https://www.health.gov.au/"},
                    {"label": "WHO", "url": "https://www.who.int/"}
                ],
                disclaimer="This is not a substitute for professional medical advice. Always consult healthcare providers for medical concerns."
            )
        
        # Extract and parse the response
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        try:
            # Remove any markdown formatting if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            result = json.loads(content)
            
            # Validate required fields
            required_fields = ["classification", "reason", "steps", "watch_for", "references", "disclaimer"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure classification is valid
            if result["classification"] not in ["self_care", "seek_care", "urgent"]:
                result["classification"] = "seek_care"
            
            return SymptomAssessmentResponse(**result)
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback to safe response if JSON parsing fails
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {content}")
            
            return SymptomAssessmentResponse(
                classification="seek_care",
                reason="Unable to process symptoms properly. Please seek medical advice.",
                steps=[
                    "Contact your healthcare provider immediately",
                    "Monitor symptoms closely",
                    "Seek emergency care if symptoms worsen",
                    "Keep a record of symptoms and their timing"
                ],
                watch_for=[
                    "Severe pain or discomfort",
                    "High fever",
                    "Difficulty breathing",
                    "Signs of severe dehydration"
                ],
                references=[
                    {"label": "Local Health", "url": "https://www.health.gov.au/"},
                    {"label": "WHO", "url": "https://www.who.int/"}
                ],
                disclaimer="This is not a substitute for professional medical advice. Always consult healthcare providers for medical concerns."
            )
    
    except Exception as e:
        print(f"Error in symptom assessment: {e}")
        raise HTTPException(
            status_code=500,
            detail="Unable to assess symptoms. Please try again or seek medical advice."
        )

@router.get("/common-symptoms")
async def get_common_symptoms():
    """
    Get common symptoms for pregnant women and infants
    """
    return {
        "pregnant": [
            "dizziness", "nausea", "headache", "fatigue", "back pain",
            "swelling", "shortness of breath", "chest pain", "abdominal pain",
            "bleeding", "contractions", "fever", "dehydration signs"
        ],
        "infant": [
            "fever", "crying", "irritability", "poor feeding", "vomiting",
            "diarrhea", "dehydration signs", "difficulty breathing", "rash",
            "lethargy", "unusual sleep", "temperature changes", "feeding refusal"
        ]
    }

@router.get("/health")
async def health_check():
    """
    Health check for symptoms API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "symptoms-assessment",
        "openai_client": "available" if client is not None else "development_mode",
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_api_key_here")
    }

@router.get("/test-openai")
async def test_openai():
    """
    Test OpenAI client functionality
    """
    if client is None:
        return {
            "status": "development_mode",
            "message": "OpenAI client not initialized - using development mode",
            "suggestion": "Check API key configuration"
        }
    
    try:
        # Test with a simple completion
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello, OpenAI is working!'"}
            ],
            max_tokens=10
        )
        
        return {
            "status": "success",
            "message": "OpenAI client is working properly",
            "response": response.choices[0].message.content.strip()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"OpenAI client test failed: {str(e)}",
            "client_initialized": True
        }
