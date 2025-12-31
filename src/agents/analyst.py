import os
import time
import google.generativeai as genai
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from langfuse.decorators import observe
from src.core.config import settings

# Inicjalizacja kluczy dla PydanticAI i Google SDK
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key
genai.configure(api_key=settings.gemini_api_key)

# --- MODELE DANYCH (M_03) ---

class ShotCandidate(BaseModel):
    """Pojedynczy fragment wideo wytypowany pod Shortsa."""
    start: str = Field(description="Znacznik czasu rozpoczęcia (MM:SS)")
    end: str = Field(description="Znacznik czasu zakończenia (MM:SS)")
    visual_description: str = Field(description="Opis warstwy wizualnej sceny")
    narrative_hook: str = Field(description="Dlaczego to przyciągnie uwagę")
    score: int = Field(description="Potencjał viralowy 1-10")

class VideoAnalysisReport(BaseModel):
    """Kompletny raport analityczny z Gemini 2.5 Flash."""
    main_topic: str = Field(description="Główny temat materiału")
    suggested_titles: List[str] = Field(description="Propozycje tytułów (max 3)")
    clips: List[ShotCandidate] = Field(description="Lista sugerowanych cięć")

# --- KONFIGURACJA AGENTA (M_06) ---

model = GoogleModel('gemini-2.5-flash')
analyst_agent = Agent(
    model=model,
    output_type=VideoAnalysisReport,
    system_prompt=(
        "Jesteś elitarnym analitykiem wideo w KUŹNI OPERATORÓW. "
        "Twoim zadaniem jest multimodalna analiza surowego materiału. "
        "Znajdź momenty o najwyższym potencjale viralowym. "
        "Bądź precyzyjny co do sekundy w znacznikach MM:SS."
    )
)

# --- LOGIKA OPERACYJNA ---

def upload_video(file_path: str):
    """Wysyła plik do Google Cloud i czeka na stan ACTIVE."""
    print(f"LOG: Przesyłanie {file_path} do Google File API...")
    media_file = genai.upload_file(path=file_path)
    
    while media_file.state.name == "PROCESSING":
        time.sleep(2)
        media_file = genai.get_file(media_file.name)
        
    if media_file.state.name == "FAILED":
        raise RuntimeError("Błąd przetwarzania pliku przez Google API.")
    
    return media_file

@observe(name="Agent_Analyst_Run")
async def run_analysis(video_path: str) -> VideoAnalysisReport:
    """Główna funkcja uruchamiająca analizę multimodalną."""
    video_handle = upload_video(video_path)
    
    print("LOG: Gemini 2.5 Flash analizuje materiał...")
    result = await analyst_agent.run(
        [
            "Wykonaj pełną analizę tego wideo pod kątem tworzenia Shorts.",
            video_handle
        ]
    )
    
    # Wersja 1.39.0 używa .output dla zwalidowanych danych
    return result.output