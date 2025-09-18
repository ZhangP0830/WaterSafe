from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os

router = APIRouter(prefix="/api/guidance", tags=["guidance"])


class GuidanceFlags(BaseModel):
    pregnant: bool = False
    postpartum: bool = False
    infant: bool = False
    immunocompromised: bool = False


class SanitationRequest(BaseModel):
    mode: str = Field(pattern="^(general|flood)$")
    place: str = Field(pattern="^(home|safe-site|rescue|temporary)$")
    profile: GuidanceFlags
    issues: List[str] = Field(default_factory=list)  # e.g., ["toilet_unusable", "no_running_water"]


class ChecklistItem(BaseModel):
    id: Optional[str] = None
    title: str
    body: Optional[str] = None  # Renamed from detail for clarity
    done: bool = False
    priority: str = "medium"  # critical, high, medium, low
    badges: List[str] = Field(default_factory=list)
    icons: List[str] = Field(default_factory=list)
    actions: List[str] = Field(default_factory=list)
    why: Optional[str] = None


class ChecklistSection(BaseModel):
    name: str
    items: List[ChecklistItem]


class ChecklistNote(BaseModel):
    type: str  # pregnancy, infant, general
    text: str


class ChecklistSource(BaseModel):
    label: str
    url: Optional[str] = None


class ChecklistResponse(BaseModel):
    summary_top3: List[ChecklistItem]
    sections: List[ChecklistSection]
    notes: List[ChecklistNote]
    sources: List[ChecklistSource]


class ExplainRequest(BaseModel):
    item_id: str
    context: dict


class ExplainResponse(BaseModel):
    explanation: str
    source: Optional[str] = None


class ChatRequest(BaseModel):
    messages: List[dict]
    context: dict
    checklist: dict


class ChatResponse(BaseModel):
    message: str
    sources: List[ChecklistSource] = Field(default_factory=list)


def _rule_based_checklist(payload: SanitationRequest) -> List[ChecklistItem]:
    mode = payload.mode
    place = payload.place
    flags = payload.flags

    items: List[ChecklistItem] = []

    # Core sanitation steps by mode
    if mode == "general":
        items.extend([
            ChecklistItem(title="Set up hand hygiene points", detail="Soap + water; ABHR (≥60%) as fallback."),
            ChecklistItem(title="Disinfect kitchen/bottle-prep surfaces", detail="Use chlorine solution; keep 1 min wet contact."),
            ChecklistItem(title="Prepare safe water for critical tasks", detail="Use bottled or cooled-boiled water."),
        ])
    else:  # flood
        items.extend([
            ChecklistItem(title="Toilet unusable: prepare bucket/liner setup", detail="Absorbent layer; ash/chlorine dosing after each use."),
            ChecklistItem(title="Separate urine/faeces where possible", detail="Reduces odour and volume."),
            ChecklistItem(title="Secure storage of sealed waste", detail="Keep away from food/child areas; covered container."),
        ])

    # Place-specific additions
    if place in ("safe-site", "rescue"):
        items.append(ChecklistItem(title="Shared facility etiquette", detail="Clean surfaces after use; signage for shared bins; queue safely."))
    if place in ("temporary",):
        items.append(ChecklistItem(title="Coordinate with host on waste storage", detail="Agree on sealed bin location; schedule for drop-off/collection."))

    # Sensitive waste guidance (always include)
    items.extend([
        ChecklistItem(title="Maternity pads/liners: sealed disposal", detail="Double-bag, seal, covered bin; cool/shaded storage if delayed collection."),
        ChecklistItem(title="Infant nappies/wipes: double-bag & date", detail="Store ≤72h; keep away from food/child zones; shared-bin etiquette in camps."),
    ])

    # Pregnancy/Infant flags to meet acceptance criteria
    if flags.pregnant:
        items.insert(0, ChecklistItem(title="Pregnancy: pads/liners OK; tampons/cups not recommended", detail="Infection risk; change frequently; safe sealed disposal."))
    if flags.infant:
        items.insert(0, ChecklistItem(title="Infant: hand hygiene before/after nappy change", detail="Disinfect change surface; keep waste sealed."))

    return items


def _generate_llm_checklist(payload: SanitationRequest) -> ChecklistResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_checklist_response(payload)
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Build context object
        context = {
            "mode": payload.mode,
            "place": payload.place,
            "profile": {
                "pregnant": payload.profile.pregnant,
                "postpartum": payload.profile.postpartum,
                "infant": payload.profile.infant,
                "immunocompromised": payload.profile.immunocompromised
            },
            "issues": payload.issues
        }

        system_prompt = (
            "You are a public-health copywriter. Write at grade-6 reading level. Use short sentences. "
            "Avoid jargon. Prefer friendly verbs. Add 'why' in one short line. Respect pregnancy/postpartum & infant safety. "
            "If advice varies by location, keep it general and ask the user to check local guidance. Never invent laws. "
            "Return valid JSON matching this exact schema: "
            '{"summary_top3": [{"title":"string","why":"string","priority":"critical|high|medium|low","badges":["string"]}], '
            '"sections": [{"name":"string","items":[{"id":"string","title":"string","body":"string","icons":["emoji"],"actions":["string"],"priority":"string"}]}], '
            '"notes": [{"type":"pregnancy|infant|general","text":"string"}], '
            '"sources": [{"label":"string","url":"string"}]}'
        )
        
        user_prompt = (
            f"Generate a sanitation checklist tailored to this context: {context}. "
            "Prioritise top 3 urgent actions. Structure as the JSON schema provided. "
            "Add pregnancy- and infant-specific notes when flags are true. Keep each item ≤ 18 words. "
            "Use calm, supportive tone."
        )

        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
        
        content = resp.choices[0].message.content.strip()
        import json
        data = json.loads(content)
        
        # Convert to our response model
        return ChecklistResponse(
            summary_top3=[ChecklistItem(**item) for item in data.get("summary_top3", [])],
            sections=[ChecklistSection(**section) for section in data.get("sections", [])],
            notes=[ChecklistNote(**note) for note in data.get("notes", [])],
            sources=[ChecklistSource(**source) for source in data.get("sources", [])]
        )
        
    except Exception as e:
        print(f"LLM error: {e}")
        return _fallback_checklist_response(payload)


def _fallback_checklist_response(payload: SanitationRequest) -> ChecklistResponse:
    """Fallback response when LLM is unavailable"""
    items = []
    
    # Add pregnancy-specific items
    if payload.profile.pregnant or payload.profile.postpartum:
        items.append(ChecklistItem(
            id="preg-pads",
            title="Use pads or liners only",
            body="Tampons and cups not safe during pregnancy",
            priority="critical",
            badges=["Pregnancy Safe"],
            icons=["🤱"],
            why="Reduces infection risk during pregnancy and recovery"
        ))
    
    # Add infant-specific items
    if payload.profile.infant:
        items.append(ChecklistItem(
            id="infant-hands",
            title="Wash hands before and after nappy changes",
            body="Use soap and water or hand sanitizer",
            priority="critical",
            badges=["Infant Priority"],
            icons=["👶", "🧼"],
            why="Infants are more vulnerable to infections"
        ))
    
    # Add general items based on mode
    if payload.mode == "flood":
        items.append(ChecklistItem(
            id="bucket-toilet",
            title="Set up a bucket toilet",
            body="Line bucket, add absorbent layer, keep separate",
            priority="high",
            icons=["🪣", "🧻"],
            why="Prevents overflow and reduces odour"
        ))
    
    return ChecklistResponse(
        summary_top3=items[:3],
        sections=[ChecklistSection(name="General Hygiene", items=items)],
        notes=[
            ChecklistNote(type="general", text="Always check local health guidance for specific requirements")
        ],
        sources=[
            ChecklistSource(label="WHO WASH Guidelines", url="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash")
        ]
    )


@router.post("/checklist", response_model=ChecklistResponse)
async def generate_checklist(payload: SanitationRequest):
    """Generate structured checklist with LLM"""
    try:
        return _generate_llm_checklist(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain", response_model=ExplainResponse)
async def explain_item(payload: ExplainRequest):
    """Get explanation for a specific checklist item"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ExplainResponse(
                explanation="This step helps maintain hygiene and safety during sanitation disruptions.",
                source="General health guidance"
            )
        
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        system_prompt = (
            "You are a calm hygiene helper. Explain why this step is important in 1-2 sentences. "
            "Use grade-6 reading level. Be supportive, not alarming. If unsure, suggest checking local guidance."
        )
        
        user_prompt = f"Explain why this checklist item is important: {payload.item_id}. Context: {payload.context}"
        
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
        
        explanation = resp.choices[0].message.content.strip()
        return ExplainResponse(explanation=explanation)
        
    except Exception as e:
        return ExplainResponse(
            explanation="This step helps maintain hygiene and safety during sanitation disruptions.",
            source="General health guidance"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(payload: ChatRequest):
    """Context-aware chat with hygiene assistant"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ChatResponse(
                message="I'm here to help with hygiene and sanitation questions. Please check local health guidance for specific requirements.",
                sources=[ChecklistSource(label="Local Health Guidance", url="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash")]
            )
        
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Build context-aware system prompt
        context_summary = f"User situation: {payload.context.get('mode', 'general')} sanitation at {payload.context.get('place', 'home')}. "
        if payload.context.get('profile', {}).get('pregnant'):
            context_summary += "User is pregnant. "
        if payload.context.get('profile', {}).get('infant'):
            context_summary += "User has an infant. "
        
        system_prompt = (
            f"You are a calm hygiene helper. Use this context: {context_summary} "
            "Keep replies short, grade-6 reading level. Offer step-by-step only when asked. "
            "Include a 'why' line if helpful. If unsure or guidance depends on local policy, say so. "
            "Avoid medical diagnosis; encourage contacting health services for concerning symptoms. "
            "Stay focused on hygiene and sanitation topics."
        )
        
        # Add context to messages
        messages = [{"role": "system", "content": system_prompt}] + payload.messages
        
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=0.4,
        )
        
        message = resp.choices[0].message.content.strip()
        
        # Extract sources from checklist if available
        sources = []
        if payload.checklist and 'sources' in payload.checklist:
            sources = [ChecklistSource(**source) for source in payload.checklist['sources']]
        
        return ChatResponse(message=message, sources=sources)
        
    except Exception as e:
        return ChatResponse(
            message="I'm here to help with hygiene and sanitation questions. Please check local health guidance for specific requirements.",
            sources=[ChecklistSource(label="Local Health Guidance", url="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash")]
        )


# Legacy endpoint for backward compatibility
@router.post("/sanitation", response_model=dict)
async def generate_sanitation_guidance(payload: SanitationRequest):
    """Legacy endpoint - redirects to new checklist format"""
    try:
        response = _generate_llm_checklist(payload)
        # Convert to legacy format for backward compatibility
        all_items = response.summary_top3 + [item for section in response.sections for item in section.items]
        return {"checklist": [item.model_dump() for item in all_items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


