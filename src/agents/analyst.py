import os
import time
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from langfuse.decorators import observe
from src.core.config import settings
from google import genai

# 1. ENVIRONMENT CONFIGURATION
# PydanticAI still uses os.environ["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

# Initialization of new SDK client for file handling
client = genai.Client(api_key=settings.gemini_api_key)

# 2. DATA MODELS (Structured Output for your PydanticAI version)
class ShotCandidate(BaseModel):
    """Represents a video fragment selected for viral potential."""
    start: str = Field(description="Fragment start timestamp (MM:SS)")
    end: str = Field(description="Fragment end timestamp (MM:SS)")
    visual_description: str = Field(description="Description of the visual layer of the scene")
    narrative_hook: str = Field(description="Why this moment will capture viewer's attention")
    score: int = Field(description="Viral potential on a scale of 1-10")

class VideoAnalysisReport(BaseModel):
    """Complete report from source material analysis."""
    main_topic: str = Field(description="Main topic and purpose of the recording")
    suggested_titles: List[str] = Field(description="Catchy title suggestions (max 3)")
    clips: List[ShotCandidate] = Field(description="List of suggested fragments to extract")

# 3. ENGINE AND AGENT INITIALIZATION
# We use the gemini-3-flash-preview model
model = GoogleModel('gemini-3-flash-preview')

analyst_agent = Agent(
    model=model,
    output_type=VideoAnalysisReport,
    system_prompt=(
        "You are an elite video analyst at OPERATORS' FORGE. "
        "Your task is multimodal analysis of raw MP4 material. "
        "Find moments with the highest viral potential that can be extracted as Shorts. "
        "CRITICAL RULES: "
        "1. Each clip must have start and end in MM:SS format. "
        "2. End time (end) MUST be greater than start time (start). "
        "3. Length of each clip must be within the range of 15 - 60 seconds. "
        "4. Never suggest time exceeding the actual duration of the material. "
        "5. Return results exclusively in VideoAnalysisReport format."
    )
)

# 4. OPERATIONAL LOGIC
@observe(name="Agent_Analyst_Run")
async def run_analysis(video_path: str, directives: str = None) -> VideoAnalysisReport:
    """Sends video to Gemini through new SDK and performs multimodal analysis."""
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: File {video_path} not found")

    print(f"LOG: Uploading {video_path} to Google File API (new SDK)...")
    
    # Upload material using new client
    video_file = client.files.upload(file=video_path)
    
    # Waiting for file processing (polling)
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)
        
    if video_file.state.name == "FAILED":
        raise RuntimeError("Error: Google API could not process the uploaded video.")
        
    print("\nLOG: Gemini 3 Flash Preview begins multimodal analysis...")
    
    # Agent invocation with video passed
    # PydanticAI for GoogleModel accepts list of objects in contents
    prompt = "Perform full analysis of this video for Shorts editing."
    if directives:
        prompt += f"\n\nCRITICAL OPERATOR DIRECTIVES: {directives}"
        
    result = await analyst_agent.run(
        prompt,
        model_settings={"contents": [{"file_data": {"mime_type": video_file.mime_type, "file_uri": video_file.uri}}]}
    )
    
    return result.output