import os
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from langfuse.decorators import observe
from src.core.config import settings

# Inicjalizacja środowiska
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

# --- MODELE DANYCH (M_03) ---

class PlatformPost(BaseModel):
    """Treść zoptymalizowana pod konkretny algorytm platformy."""
    platform: str = Field(description="TikTok, YouTube lub LinkedIn")
    content: str = Field(description="Pełny tekst posta")
    hashtags: List[str] = Field(description="Lista hashtagów")

class CampaignBrief(BaseModel):
    """Finalna strategia marketingowa wygenerowana przez Agenta."""
    overall_strategy: str = Field(description="Kąt narracyjny kampanii")
    posts: List[PlatformPost] = Field(description="Zestaw postów")

# --- KONFIGURACJA AGENTA (M_06) ---

model = GoogleModel('gemini-2.5-flash')
copywriter_agent = Agent(
    model=model,
    output_type=CampaignBrief,
    system_prompt=(
        "Jesteś Szefem Strategii Contentowej w KUŹNI OPERATORÓW. "
        "Na podstawie dostarczonego raportu analitycznego przygotuj kampanię. "
        "Dostosuj styl: TikTok (hooki), LinkedIn (autorytet), YouTube (SEO). "
        "Pisz wyłącznie po polsku."
    )
)

# --- LOGIKA OPERACYJNA ---

@observe(name="Agent_Copywriter_Run")
async def run_copywriting(analysis_data: dict) -> CampaignBrief:
    """Przetwarza dane analityczne na posty social media."""
    print("LOG: Generowanie strategii copywriterskiej...")
    
    result = await copywriter_agent.run(
        f"Przygotuj kampanię dla tych danych: {analysis_data}"
    )
    
    return result.output