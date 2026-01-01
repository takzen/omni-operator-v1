import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def timestamp_to_seconds(ts: str) -> float:
    """Konwertuje format MM:SS na sekundy."""
    try:
        parts = ts.split(':')
        return float(int(parts[0]) * 60 + int(parts[1]))
    except:
        return 0.0

def process_video_segments(source_path: str, clips_data: list, job_id: str, output_root: str = None):
    """Wycina klipy i zapisuje je w folderze publicznym."""
    if output_root is None:
        output_root = os.path.join("web", "public", "output")
        
    output_base = os.path.join(output_root, job_id)
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
            
            # ZABEZPIECZENIE: Nie wycinamy poza czas trwania filmu
            end_s = min(end_s, video.duration)

            # Safety Guard: Max 90 seconds per clip
            if (end_s - start_s) > 90:
                print(f"⚠️ OSTRZEŻENIE: Klip {i} jest za długi ({end_s - start_s}s). Przycinam do 60s.")
                end_s = start_s + 60

            if start_s >= end_s:
                print(f"WARN: Segment {i} jest nieprawidłowy (start >= end). Pomijam.")
                continue
                
            # 1. Wycięcie fragmentu
            source_clip = video.subclipped(start_s, end_s)
            
            # 2. Automatyczne kadrowanie do 9:16 (Pionowe wideo pod Shorts/TikTok)
            w, h = source_clip.size
            target_ratio = 9/16
            new_h = h
            new_w = int(h * target_ratio)
            
            # Sprawdzenie czy wideo nie jest już pionowe lub węższe niż 9:16
            if new_w > w:
                new_w = w
                new_h = int(w / target_ratio)
                
            final_clip = source_clip.cropped(
                x_center=w/2, 
                y_center=h/2, 
                width=new_w, 
                height=new_h
            )
            
            # 3. Dodanie paska brandingowego KUŹNI OPERATORÓW
            from moviepy.video.VideoClip import ColorClip
            from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
            
            try:
                # Pasek o wysokości 5% ekranu na dole w kolorze Dark Red
                brand_overlay = ColorClip(
                    size=(new_w, int(new_h * 0.05)), 
                    color=(139, 0, 0) # #8B0000
                ).with_duration(final_clip.duration).with_opacity(0.8).with_position(("center", "bottom"))
                
                output_clip = CompositeVideoClip([final_clip, brand_overlay])
            except Exception as e:
                print(f"WARN: Błąd przy nakładaniu brandingu: {e}. Renderuję czysty pion.")
                output_clip = final_clip
            
            # 4. Render finalny
            output_clip.write_videofile(target_path, codec="libx264", audio_codec="aac", logger=None)
            
            # URL względny dla Next.js
            generated_files.append({
                "url": f"/output/{job_id}/{file_name}",
                "hook": clip.get('narrative_hook', 'Brak opisu')
            })
            
    return generated_files