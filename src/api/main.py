from fastapi import FastAPI, BackgroundTasks
from src.core.config import settings
from src.services.video_engine import process_shorts
# Tu zaimportujesz swoich Agentów

app = FastAPI(title="OMNI-OPERATOR-V1")

@app.post("/run-mission")
async def run_mission(video_path: str, background_tasks: BackgroundTasks):
    # Tutaj spniemy cały workflow: 
    # 1. Analyst.run()
    # 2. Copywriter.run()
    # 3. process_shorts()
    # 4. Save to Qdrant
    return {"message": "Mission initiated", "video": video_path}