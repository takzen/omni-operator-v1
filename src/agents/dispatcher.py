import os
import shutil
from typing import List
from pydantic_ai import Agent, Tool
from pydantic_ai.models.google import GoogleModel
from langfuse.decorators import observe
from src.core.config import settings

# 1. ENGINE INITIALIZATION
model = GoogleModel('gemini-3-flash-preview')

class DistributionCenter:
    """Handles physical file operations for content distribution."""
    
    def __init__(self, job_output_dir: str):
        self.job_output_dir = job_output_dir

    def move_to_platform_folder(self, filename: str, platform: str) -> str:
        """
        Copies a video clip to a platform-specific subfolder with a descriptive name.
        Example: short_1.mp4 -> {job_dir}/tiktok/tiktok_short_1.mp4
        """
        platform = platform.lower().strip()
        target_dir = os.path.join(self.job_output_dir, platform)
        os.makedirs(target_dir, exist_ok=True)
        
        # New descriptive filename
        new_filename = f"{platform}_{filename}"
        
        src_path = os.path.join(self.job_output_dir, filename)
        dst_path = os.path.join(target_dir, new_filename)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            return f"SUCCESS: {new_filename} distributed to {platform.upper()}."
        return f"ERROR: File {filename} not found."

@observe(name="Agent_Dispatcher_Run")
async def run_dispatch(job_id: str, web_output_root: str, campaign_data: dict):
    """
    Dispatcher Agent: Analyzes the campaign strategy and physically organizes files 
    into platform-specific folders.
    """
    print(f"LOG [{job_id}]: Entering run_dispatch function...", flush=True)
    
    # 1. Organization in web folder (for Next.js)
    job_web_dir = os.path.join(web_output_root, job_id)
    print(f"LOG [{job_id}]: Web job directory: {job_web_dir}", flush=True)
    distributor_web = DistributionCenter(job_web_dir)
    
    # 2. Organization in root 'output' folder (for the Operator)
    root_output_dir = os.path.join(os.getcwd(), "output", job_id)
    os.makedirs(root_output_dir, exist_ok=True)
    print(f"LOG [{job_id}]: Root output directory: {root_output_dir}", flush=True)
    
    # Copy original files to root output first
    files_to_copy = os.listdir(job_web_dir)
    print(f"LOG [{job_id}]: Found {len(files_to_copy)} files in web dir.", flush=True)
    for f in files_to_copy:
        if f.endswith(".mp4") and os.path.isfile(os.path.join(job_web_dir, f)):
            print(f"LOG [{job_id}]: Copying {f} to root output...", flush=True)
            shutil.copy2(os.path.join(job_web_dir, f), os.path.join(root_output_dir, f))
            
    distributor_root = DistributionCenter(root_output_dir)
    
    def dual_distribute(filename: str, platform: str) -> str:
        print(f"TOOL_CALL [{job_id}]: Distributing {filename} to {platform}...", flush=True)
        res1 = distributor_web.move_to_platform_folder(filename, platform)
        res2 = distributor_root.move_to_platform_folder(filename, platform)
        result = f"Web: {res1} | Root: {res2}"
        print(f"TOOL_RESULT [{job_id}]: {result}", flush=True)
        return result

    distribution_tool = Tool(
        dual_distribute,
        name="move_video_to_platform",
        description="Organizes video files into platform-specific folders (tiktok, youtube, linkedin)."
    )
    
    dispatcher_agent = Agent(
        model=model,
        tools=[distribution_tool],
        system_prompt=(
            "You are the Logistics Coordinator at OPERATORS' FORGE. "
            "Your mission is to distribute produced video clips into their respective platform folders. "
            f"Current Mission ID: {job_id}. "
            "\n\nRULES:\n"
            "1. Analyze the 'clip_strategies' in the provided campaign data.\n"
            "2. Each strategy has a 'clip_index' (e.g., 1) and a list of 'posts'.\n"
            "3. Each post has a 'platform' (e.g., 'TikTok').\n"
            "4. For each post, move the file 'short_{clip_index}.mp4' to the corresponding platform folder.\n"
            "5. ONLY move a file to a platform if a post for that specific clip and platform exists.\n"
            "6. Be precise. Do not duplicate assignments if not requested."
        )
    )
    
    print(f"LOG [{job_id}]: Agent Dispatcher starting selective distribution...", flush=True)
    
    # We pass only necessary data to save tokens and potentially quota impact
    strategies = campaign_data.get('clip_strategies', [])
    minimal_strategy = []
    
    for cs in strategies:
        if isinstance(cs, dict):
            c_idx = cs.get('clip_index')
            plats = [p.get('platform', '').lower().strip() for p in cs.get('posts', [])]
        else:
            c_idx = cs.clip_index
            plats = [p.platform.lower().strip() for p in cs.posts]
            
        minimal_strategy.append({
            "clip_index": c_idx,
            "platforms": plats
        })
    
    prompt = (
        f"Analyze this assignment strategy: {minimal_strategy}. "
        "Your task is to call 'move_video_to_platform' ONLY for the specific (clip, platform) pairs listed. "
        "Rule: If clip 1 is for TikTok, call it. If clip 1 is NOT listed for LinkedIn, DO NOT call it. "
        "Execute now for all pairs."
    )
    
    result = await dispatcher_agent.run(prompt)
    
    print(f"LOG [{job_id}]: Agent Dispatcher finished selective mission.", flush=True)
    
    return True
