import os
import sys
import uuid
import shutil
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 1. KRYTYCZNE: USTAWIE ŚCIEŻEK PROJEKTU
# Pozwala na importowanie modułów z folderu 'src' niezależnie od miejsca uruchomienia
root_path = str(Path(__file__).parent.parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

# Ładowanie zmiennych środowiskowych z pliku .env w ROOT
load_dotenv(os.path.join(root_path, ".env"))

from src.core.config import settings
from src.agents.analyst import run_analysis
from src.agents.copywriter import run_copywriting
from src.services.video_proc import process_video_segments

# 2. KONFIGURACJA ŚRODOWISKA DLA LANGFUSE I GEMINI
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
os.environ["LANGFUSE_HOST"] = settings.langfuse_host

# 3. INICJALIZACJA API
app = FastAPI(title="OMNI-OPERATOR-V1 // API")

# Pozwalamy Next.js (port 4000) na pełną komunikację z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na etapie dev pozwalamy na wszystkie źródła
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tworzymy foldery na dane, jeśli nie istnieją
root_path_obj = Path(__file__).resolve().parent.parent.parent
temp_dir = root_path_obj / "temp"
output_dir = root_path_obj / "web" / "public" / "output"

temp_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

print(f"LOG: Serving static files from: {output_dir}")

# SŁUŻYMY PLIKAMI STATYCZNYMI (GŁÓWNIE WIDEO)
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")

# Baza zadań w pamięci RAM
jobs = {}

# --- ENDPOINTY ---

@app.get("/")
async def health_check():
    return {"status": "OPERATIONAL", "engine": "GEMINI 3 FLASH PREVIEW"}

@app.post("/upload")
async def start_mission(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Przyjmuje plik wideo i inicjuje asynchroniczny workflow."""
    job_id = str(uuid.uuid4())[:8]
    temp_path = os.path.join(temp_dir, f"{job_id}_{file.filename}")
    
    # Zapis pliku na dysku serwera
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Inicjalizacja stanu zadania
    jobs[job_id] = {
        "job_id": job_id,
        "status": "ANALYZING",
        "video_path": temp_path,
        "result": None
    }
    
    # Uruchomienie "Pociągu Montażowego" w tle
    background_tasks.add_task(execute_workflow, job_id, temp_path)
    
    return {"job_id": job_id, "status": "STARTED"}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Zwraca aktualny stan zadania dla frontendu."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Mission not found")
    return jobs[job_id]

# --- WORKFLOW DYRYGENTA ---

async def execute_workflow(job_id: str, video_path: str):
    """Orkiestracja wszystkich modułów systemu."""
    try:
        # KROK 1: Multimodalna Analiza Gemini 3 Flash Preview
        print(f"LOG [{job_id}]: Start analizy wizualnej...")
        analysis_report = await run_analysis(video_path)
        
        # KROK 2: Generowanie Strategii i Postów (Agent Copywriter)
        jobs[job_id]["status"] = "WRITING"
        print(f"LOG [{job_id}]: Gemini generuje posty social media...")
        campaign = await run_copywriting(analysis_report.model_dump())
        
        # KROK 3: Fizyczny Montaż FFmpeg (Video Proc)
        jobs[job_id]["status"] = "RENDERING"
        print(f"LOG [{job_id}]: System tnie wideo na fragmenty...")
        video_results = process_video_segments(
            video_path, 
            analysis_report.model_dump()['clips'], 
            job_id,
            output_root=output_dir
        )
        
        # FINALIZACJA: Zapisanie wyników dla frontendu
        jobs[job_id]["status"] = "COMPLETED"
        jobs[job_id]["result"] = {
            "campaign": campaign.model_dump(),
            "videos": video_results
        }
        
        # KROK 4: Pamięć Długotrwała (Qdrant)
        try:
            from src.services.memory import save_campaign_to_memory
            # Używamy tematu z raportu analitycznego jako klucza
            topic = analysis_report.main_topic
            save_campaign_to_memory(
                {**campaign.model_dump(), "job_id": job_id}, 
                topic
            )
        except Exception as mem_err:
            print(f"WARN [{job_id}]: Nie udało się zapisać w pamięci Qdrant: {mem_err}")

        print(f"✅ LOG [{job_id}]: Misja zakończona sukcesem.")

    except Exception as e:
        jobs[job_id]["status"] = "FAILED"
        jobs[job_id]["error"] = str(e)
        print(f"❌ LOG [{job_id}]: BŁĄD KRYTYCZNY: {e}")

# --- START SERWERA ---

if __name__ == "__main__":
    import uvicorn
    # Uruchomienie na porcie 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)