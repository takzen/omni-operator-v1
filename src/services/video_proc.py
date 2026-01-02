import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def timestamp_to_seconds(ts: str) -> float:
    """Converts MM:SS format to seconds."""
    try:
        parts = ts.split(':')
        return float(int(parts[0]) * 60 + int(parts[1]))
    except:
        return 0.0

def process_video_segments(source_path: str, clips_data: list, job_id: str, output_root: str = None):
    """Cuts clips and saves them in public folder."""
    if output_root is None:
        output_root = os.path.join("web", "public", "output")
        
    output_base = os.path.join(output_root, job_id)
    os.makedirs(output_base, exist_ok=True)
    
    generated_files = []
    
    print(f"LOG: Starting editing for Job: {job_id}")
    
    with VideoFileClip(source_path) as video:
        for i, clip in enumerate(clips_data, 1):
            start_s = timestamp_to_seconds(clip['start'])
            end_s = timestamp_to_seconds(clip['end'])
            
            file_name = f"short_{i}.mp4"
            target_path = os.path.join(output_base, file_name)
            
            print(f"LOG: Rendering fragment {i}...")
            
            # SAFETY: We don't cut beyond video duration
            end_s = min(end_s, video.duration)

            # Safety Guard: Max 90 seconds per clip
            if (end_s - start_s) > 90:
                print(f"⚠️ WARNING: Clip {i} is too long ({end_s - start_s}s). Trimming to 60s.")
                end_s = start_s + 60

            if start_s >= end_s:
                print(f"WARN: Segment {i} is invalid (start >= end). Skipping.")
                continue
                
            # 1. Fragment extraction
            source_clip = video.subclipped(start_s, end_s)
            
            # 2. Automatic cropping to 9:16 (Vertical video for Shorts/TikTok)
            w, h = source_clip.size
            target_ratio = 9/16
            new_h = h
            new_w = int(h * target_ratio)
            
            # Check if video is not already vertical or narrower than 9:16
            if new_w > w:
                new_w = w
                new_h = int(w / target_ratio)
                
            final_clip = source_clip.cropped(
                x_center=w/2, 
                y_center=h/2, 
                width=new_w, 
                height=new_h
            )
            
            # 3. Adding OPERATORS' FORGE branding bar
            from moviepy.video.VideoClip import ColorClip
            from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
            
            try:
                # Bar with height of 5% of screen at bottom in Dark Red color
                brand_overlay = ColorClip(
                    size=(new_w, int(new_h * 0.05)), 
                    color=(139, 0, 0) # #8B0000
                ).with_duration(final_clip.duration).with_opacity(0.8).with_position(("center", "bottom"))
                
                output_clip = CompositeVideoClip([final_clip, brand_overlay])
            except Exception as e:
                print(f"WARN: Error applying branding: {e}. Rendering clean vertical.")
                output_clip = final_clip
            
            # 4. Final render
            output_clip.write_videofile(target_path, codec="libx264", audio_codec="aac", logger=None)
            
            # Relative URL for Next.js
            generated_files.append({
                "url": f"/output/{job_id}/{file_name}",
                "hook": clip.get('narrative_hook', 'No description')
            })
            
    return generated_files