import os
import time
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from langfuse.decorators import observe
from src.core.config import settings
from google import genai

# 1. KONFIGURACJA ŚRODOWISKA
# PydanticAI nadal korzysta z os.environ["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

# Inicjalizacja nowego klienta SDK do obsługi plików
client = genai.Client(api_key=settings.gemini_api_key)

# 2. MODELE DANYCH (Structured Output dla Twojej wersji PydanticAI)
class ShotCandidate(BaseModel):
    """Reprezentuje fragment wideo wyselekcjonowany pod kątem viralowym."""
    start: str = Field(description="Znacznik czasu rozpoczęcia fragmentu (MM:SS)")
    end: str = Field(description="Znacznik czasu zakończenia fragmentu (MM:SS)")
    visual_description: str = Field(description="Opis warstwy wizualnej sceny")
    narrative_hook: str = Field(description="Dlaczego ten moment przyciągnie uwagę widza")
    score: int = Field(description="Potencjał viralowy w skali 1-10")

class VideoAnalysisReport(BaseModel):
    """Kompletny raport z analizy materiału źródłowego."""
    main_topic: str = Field(description="Główny temat i cel nagrania")
    suggested_titles: List[str] = Field(description="Propozycje chwytliwych tytułów (max 3)")
    clips: List[ShotCandidate] = Field(description="Lista sugerowanych fragmentów do wycięcia")

# 3. INICJALIZACJA SILNIKA I AGENTA
# Używamy modelu gemini-3-flash-preview
model = GoogleModel('gemini-3-flash-preview')

analyst_agent = Agent(
    model=model,
    output_type=VideoAnalysisReport,
    system_prompt=(
        "Jesteś elitarnym analitykiem wideo w KUŹNI OPERATORÓW. "
        "Twoim zadaniem jest multimodalna analiza surowego materiału MP4. "
        "Znajdź momenty o najwyższym potencjale viralowym, które można wyciąć jako Shortsy. "
        "KRYTYCZNE ZASADY: "
        "1. Każdy klip musi mieć start i end w formacie MM:SS. "
        "2. Czas końcowy (end) MUSI być większy niż czas początkowy (start). "
        "3. Nigdy nie sugeruj czasu wykraczającego poza faktyczny czas trwania materiału. "
        "4. Zwracaj wyniki wyłącznie w formacie VideoAnalysisReport."
    )
)

# 4. LOGIKA OPERACYJNA
@observe(name="Agent_Analyst_Run")
async def run_analysis(video_path: str) -> VideoAnalysisReport:
    """Wysyła wideo do Gemini przez nowe SDK i przeprowadza analizę multimodalną."""
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Błąd: Nie znaleziono pliku {video_path}")

    print(f"LOG: Przesyłanie {video_path} do Google File API (nowe SDK)...")
    
    # Upload materiału przy użyciu nowego klienta
    video_file = client.files.upload(file=video_path)
    
    # Oczekiwanie na przetworzenie pliku (polling)
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)
        
    if video_file.state.name == "FAILED":
        raise RuntimeError("Błąd: Google API nie mogło przetworzyć przesłanego wideo.")
        
    print("\nLOG: Gemini 3 Flash Preview rozpoczyna analizę multimodalną...")
    
    # Wywołanie agenta z przekazaniem wideo
    # PydanticAI dla GoogleModel przyjmuje listę obiektów w contents
    result = await analyst_agent.run(
        "Wykonaj pełną analizę tego wideo pod kątem montażu Shorts.",
        model_settings={"contents": [{"file_data": {"mime_type": video_file.mime_type, "file_uri": video_file.uri}}]}
    )
    
    return result.output