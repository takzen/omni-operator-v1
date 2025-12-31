import os
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from langfuse.decorators import observe
from src.core.config import settings

# 1. KONFIGURACJA ŚRODOWISKA
# PydanticAI wymaga GOOGLE_API_KEY w os.environ
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

# 2. MODELE DANYCH (Structured Output)
class PlatformPost(BaseModel):
    """Pojedyncza treść zoptymalizowana pod algorytm danej platformy."""
    platform: str = Field(description="TikTok, YouTube lub LinkedIn")
    content: str = Field(description="Pełna treść posta wraz z hookiem i CTA")
    hashtags: List[str] = Field(description="Lista celowanych hashtagów")

class ClipStrategy(BaseModel):
    """Strategia marketingowa dla pojedynczego fragmentu wideo."""
    clip_index: int = Field(description="Numer porządkowy klipu z analizy")
    posts: List[PlatformPost] = Field(description="Warianty treści na platformy")

class CampaignBrief(BaseModel):
    """Finalna strategia marketingowa wygenerowana przez Agenta."""
    overall_strategy: str = Field(description="Główna idea i ton kampanii")
    clip_strategies: List[ClipStrategy] = Field(description="Szczegółowe posty dla każdego klipu")

# 3. INICJALIZACJA SILNIKA I AGENTA
# Używamy modelu gemini-2.5-flash
model = GoogleModel('gemini-2.5-flash')

copywriter_agent = Agent(
    model=model,
    output_type=CampaignBrief, # Standard dla Twojej wersji pydantic-ai
    system_prompt=(
        "Jesteś Szefem Strategii Contentowej w KUŹNI OPERATORÓW. "
        "Twoim zadaniem jest tworzenie treści social media na podstawie danych technicznych. "
        "Dla każdego materiału przygotuj: "
        "1. TikTok: Agresywny hook, szybkie tempo, slang branżowy. "
        "2. YouTube: Skupienie na wartości edukacyjnej i SEO. "
        "3. LinkedIn: Merytoryczny wgląd, budowanie autorytetu, storytelling. "
        "Pisz wyłącznie po polsku."
    )
)

# 4. LOGIKA OPERACYJNA
@observe(name="Agent_Copywriter_Run")
async def run_copywriting(analysis_data: dict) -> CampaignBrief:
    """Transformuje dane analityczne na kompletną kampanię postów."""
    
    print("LOG: Gemini 2.5 Flash generuje strategię i posty social media...")
    
    result = await copywriter_agent.run(
        f"Przygotuj kampanię marketingową na podstawie następujących danych analitycznych: {analysis_data}"
    )
    
    # Zgodnie z wersją 1.39.0 wynik znajduje się w .output
    return result.output