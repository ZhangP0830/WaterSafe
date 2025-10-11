from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import hashlib
import json
import time
import logging

router = APIRouter(prefix="/api/guidance", tags=["guidance"])

# In-memory cache for checklist responses
# Structure: {hash: {"data": ChecklistResponse, "ts": timestamp}}
_checklist_cache = {}

# Cache TTL in seconds (15 minutes)
CACHE_TTL = 15 * 60

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GuidanceFlags(BaseModel):
    pregnant: bool = False
    infant: bool = False


class SanitationRequest(BaseModel):
    mode: str = Field(pattern="^(general|flood)$")
    place: str = Field(pattern="^(home|safe-site|rescue|temporary)$")
    profile: GuidanceFlags
    issues: List[str] = Field(default_factory=list)  # e.g., ["toilet_unusable", "no_running_water"]


class ChecklistSource(BaseModel):
    label: str
    url: Optional[str] = None


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
    sources: List[ChecklistSource] = Field(default_factory=list)  # References per item


class ChecklistSection(BaseModel):
    name: str
    items: List[ChecklistItem]


class ChecklistNote(BaseModel):
    type: str  # pregnancy, infant, general
    text: str


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
    sources: List[dict] = Field(default_factory=list)  # Sources from checklist items


class ChatResponse(BaseModel):
    message: str
    sources: List[ChecklistSource] = Field(default_factory=list)


def _generate_context_hash(context: dict) -> str:
    """Generate SHA256 hash of context for caching"""
    context_str = json.dumps(context, sort_keys=True)
    return hashlib.sha256(context_str.encode()).hexdigest()


def _is_cache_valid(timestamp: float) -> bool:
    """Check if cache entry is still valid based on TTL"""
    return (time.time() - timestamp) < CACHE_TTL


def _clean_expired_cache():
    """Remove expired entries from cache"""
    current_time = time.time()
    expired_keys = [
        key for key, value in _checklist_cache.items()
        if (current_time - value["ts"]) >= CACHE_TTL
    ]
    for key in expired_keys:
        del _checklist_cache[key]
    if expired_keys:
        logger.info(f"Cleaned {len(expired_keys)} expired cache entries")


def _rule_based_checklist(payload: SanitationRequest) -> List[ChecklistItem]:
    mode = payload.mode
    place = payload.place
    flags = payload.profile

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
                "infant": payload.profile.infant
            },
            "issues": payload.issues
        }

        system_prompt = (
            "You are a public-health copywriter. Write at grade-6 reading level. Use short sentences. "
            "Avoid jargon. Prefer friendly verbs. Add 'why' in one short line. Respect pregnancy/postpartum & infant safety. "
            "If advice varies by location, keep it general and ask the user to check local guidance. Never invent laws. "
            "IMPORTANT: Each checklist item MUST include relevant source references from WHO, CDC, or local health authorities. "
            "Return valid JSON matching this exact schema: "
            '{"summary_top3": [{"title":"string","why":"string","priority":"critical|high|medium|low","badges":["string"],"sources":[{"label":"string","url":"string"}]}], '
            '"sections": [{"name":"string","items":[{"id":"string","title":"string","body":"string","icons":["emoji"],"actions":["string"],"priority":"string","sources":[{"label":"string","url":"string"}]}]}], '
            '"notes": [{"type":"pregnancy|infant|general","text":"string"}], '
            '"sources": [{"label":"string","url":"string"}]}'
        )
        
        user_prompt = (
            f"Generate a sanitation checklist tailored to this context: {context}. "
            "Prioritise top 3 urgent actions. Structure as the JSON schema provided. "
            "Add pregnancy- and infant-specific notes when flags are true. Keep each item ≤ 18 words. "
            "Use calm, supportive tone. "
            "CRITICAL: Include authoritative sources (WHO, CDC, local health) for each checklist item. "
            "Use real URLs like https://www.who.int/health-topics/water-sanitation-and-hygiene-wash or https://www.cdc.gov/hygiene/index.html"
        )

        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18"),
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
    if payload.profile.pregnant:
        items.append(ChecklistItem(
            id="preg-pads",
            title="Use pads or liners only",
            body="Tampons and cups not safe during pregnancy",
            priority="critical",
            badges=["Pregnancy Safe"],
            icons=["🤱"],
            why="Reduces infection risk during pregnancy",
            sources=[
                ChecklistSource(label="WHO", url="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash"),
                ChecklistSource(label="CDC", url="https://www.cdc.gov/hygiene/index.html")
            ]
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
            why="Infants are more vulnerable to infections",
            sources=[
                ChecklistSource(label="WHO", url="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash"),
                ChecklistSource(label="CDC", url="https://www.cdc.gov/hygiene/index.html")
            ]
        ))
    
    # Add general items based on mode
    if payload.mode == "flood":
        items.append(ChecklistItem(
            id="bucket-toilet",
            title="Set up a bucket toilet",
            body="Line bucket, add absorbent layer, keep separate",
            priority="high",
            icons=["🪣", "🧻"],
            why="Prevents overflow and reduces odour",
            sources=[
                ChecklistSource(label="WHO", url="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash")
            ]
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
async def generate_checklist(
    payload: SanitationRequest,
    force: bool = Query(False, description="Force fresh LLM call, bypass cache")
):
    """Generate structured checklist with LLM and caching"""
    try:
        # Build context for hashing
        context = {
            "mode": payload.mode,
            "place": payload.place,
            "profile": {
                "pregnant": payload.profile.pregnant,
                "infant": payload.profile.infant
            },
            "issues": payload.issues
        }
        
        # Generate context hash
        context_hash = _generate_context_hash(context)
        
        # Clean expired cache entries
        _clean_expired_cache()
        
        # Check cache first (unless force=true)
        cache_hit = False
        llm_call = False
        
        if not force and context_hash in _checklist_cache:
            cached_entry = _checklist_cache[context_hash]
            if _is_cache_valid(cached_entry["ts"]):
                cache_hit = True
                logger.info(f"Cache hit for hash: {context_hash[:8]}...")
                return cached_entry["data"]
            else:
                # Remove expired entry
                del _checklist_cache[context_hash]
                logger.info(f"Removed expired cache entry for hash: {context_hash[:8]}...")
        
        # Generate fresh response
        llm_call = True
        logger.info(f"LLM call for hash: {context_hash[:8]}... (force={force}, cache_hit={cache_hit})")
        
        response = _generate_llm_checklist(payload)
        
        # Store in cache
        _checklist_cache[context_hash] = {
            "data": response,
            "ts": time.time()
        }
        
        logger.info(f"Stored response in cache for hash: {context_hash[:8]}... (llm_call={llm_call}, cache_hit={cache_hit})")
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating checklist: {str(e)}")
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
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18"),
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
        
        # Build available sources context
        available_sources = []
        if payload.sources:
            available_sources = [ChecklistSource(**source) for source in payload.sources]
        
        sources_context = ""
        if available_sources:
            sources_list = ", ".join([f"{source.label} ({source.url})" for source in available_sources])
            sources_context = f" Available authoritative sources: {sources_list}."
        
        system_prompt = (
            f"You are a calm hygiene helper. Use this context: {context_summary} "
            "Keep replies short, grade-6 reading level. Offer step-by-step only when asked. "
            "Include a 'why' line if helpful. If unsure or guidance depends on local policy, say so. "
            "Avoid medical diagnosis; encourage contacting health services for concerning symptoms. "
            "Stay focused on hygiene and sanitation topics."
            f"{sources_context} "
            "When providing information, cite relevant sources from the available list when appropriate."
        )
        
        # Add context to messages
        messages = [{"role": "system", "content": system_prompt}] + payload.messages
        
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18"),
            messages=messages,
            temperature=0.4,
        )
        
        message = resp.choices[0].message.content.strip()
        
        # Use sources from request (collected from checklist items)
        sources = available_sources if available_sources else []
        
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


