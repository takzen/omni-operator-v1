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

# 1. CRITICAL: PROJECT PATH SETUP
# Allows importing modules from 'src' folder regardless of launch location
root_path = str(Path(__file__).parent.parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

# Loading environment variables from .env file in ROOT
load_dotenv(os.path.join(root_path, ".env"))

from src.core.config import settings
from src.agents.analyst import run_analysis
from src.agents.copywriter import run_copywriting
from src.services.video_proc import process_video_segments
from src.agents.dispatcher import run_dispatch

# 2. ENVIRONMENT CONFIGURATION FOR LANGFUSE AND GEMINI
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
os.environ["LANGFUSE_HOST"] = settings.langfuse_host

# 3. API INITIALIZATION
app = FastAPI(title="OMNI-OPERATOR-V1 // API")

# We allow Next.js (port 4000) full communication with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # At dev stage we allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We create folders for data if they don't exist
root_path_obj = Path(__file__).resolve().parent.parent.parent
temp_dir = root_path_obj / "temp"
output_dir = root_path_obj / "web" / "public" / "output"

temp_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

print(f"LOG: Serving static files from: {output_dir}")

# WE SERVE STATIC FILES (MAINLY VIDEO)
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")

# Job database in RAM
jobs = {}

# --- ENDPOINTS ---

@app.get("/")
async def health_check():
    return {"status": "OPERATIONAL", "engine": "GEMINI 3 FLASH PREVIEW"}

@app.post("/upload")
async def start_mission(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Accepts video file and initiates asynchronous workflow."""
    job_id = str(uuid.uuid4())[:8]
    temp_path = os.path.join(temp_dir, f"{job_id}_{file.filename}")
    
    # Saving file on server disk
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Task state initialization
    jobs[job_id] = {
        "job_id": job_id,
        "status": "ANALYZING",
        "video_path": temp_path,
        "result": None
    }
    
    # Launching "Editing Train" in background
    background_tasks.add_task(execute_workflow, job_id, temp_path)
    
    return {"job_id": job_id, "status": "STARTED"}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Returns current task state for frontend."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Mission not found")
    return jobs[job_id]

# --- CONDUCTOR WORKFLOW ---

async def execute_workflow(job_id: str, video_path: str):
    """Orchestration of all system modules."""
    try:
        # STEP 1: Multimodal Analysis Gemini 3 Flash Preview
        print(f"LOG [{job_id}]: Starting visual analysis...")
        analysis_report = await run_analysis(video_path)
        
        # STEP 2: Strategy and Posts Generation (Copywriter Agent)
        jobs[job_id]["status"] = "WRITING"
        print(f"LOG [{job_id}]: Gemini generating social media posts...")
        campaign = await run_copywriting(analysis_report.model_dump())
        
        # STEP 3: Physical FFmpeg Editing (Video Proc)
        jobs[job_id]["status"] = "RENDERING"
        print(f"LOG [{job_id}]: System cutting video into fragments...")
        video_results = process_video_segments(
            video_path, 
            analysis_report.model_dump()['clips'], 
            job_id,
            output_root=output_dir
        )
        
        # STEP 4: Strategic Distribution (Dispatcher Agent / MCP)
        jobs[job_id]["status"] = "DISTRIBUTING"
        print(f"LOG [{job_id}]: Agent Dispatcher organizing assets...", flush=True)
        await run_dispatch(job_id, output_dir, campaign.model_dump())
        
        # FINALIZATION: Saving results for frontend
        jobs[job_id]["status"] = "COMPLETED"
        jobs[job_id]["result"] = {
            "campaign": campaign.model_dump(),
            "videos": video_results
        }
        
        # STEP 4: Long-term Memory (Qdrant)
        try:
            from src.services.memory import save_campaign_to_memory
            # We use topic from analytical report as key
            topic = analysis_report.main_topic
            save_campaign_to_memory(
                {**campaign.model_dump(), "job_id": job_id}, 
                topic
            )
        except Exception as mem_err:
            print(f"WARN [{job_id}]: Failed to save in Qdrant memory: {mem_err}")

        print(f"✅ LOG [{job_id}]: Mission completed successfully.")

    except Exception as e:
        jobs[job_id]["status"] = "FAILED"
        jobs[job_id]["error"] = str(e)
        print(f"❌ LOG [{job_id}]: CRITICAL ERROR: {e}")

# --- SERVER START ---

if __name__ == "__main__":
    import uvicorn
    # Launch on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)