import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def timestamp_to_seconds(ts: str) -> float:
    """Konwertuje format MM:SS na sekundy."""
    try:
        parts = ts.split(':')
        return float(int(parts[0]) * 60 + int(parts[1]))
    except:
        return 0.0

def process_video_segments(source_path: str, clips_data: list, job_id: str):
    """Wycina klipy i zapisuje je w folderze publicznym Next.js."""
    # Ścieżka do folderu publicznego Twojego frontendu
    output_base = os.path.join("web", "public", "output", job_id)
    os.makedirs(output_base, exist_ok=True)
    
    generated_files = []
    
    print(f"LOG: Rozpoczynam montaż dla Job: {job_id}")
    
    with VideoFileClip(source_path) as video:
        for i, clip in enumerate(clips_data, 1):
            start_s = timestamp_to_seconds(clip['start'])
            end_s = timestamp_to_seconds(clip['end'])
            
            file_name = f"short_{i}.mp4"
            target_path = os.path.join(output_base, file_name)
            
            print(f"LOG: Renderowanie fragmentu {i}...")
            # MoviePy v2.x standard
            new_clip = video.subclipped(start_s, end_s)
            new_clip.write_videofile(target_path, codec="libx264", audio_codec="aac", logger=None)
            
            # URL względny dla Next.js
            generated_files.append({
                "url": f"/output/{job_id}/{file_name}",
                "hook": clip.get('narrative_hook', 'Brak opisu')
            })
            
    return generated_files