import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def timestamp_to_seconds(ts: str) -> float:
    minutes, seconds = map(int, ts.split(':'))
    return float(minutes * 60 + seconds)

def process_shorts(source_path: str, clips: list):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    with VideoFileClip(source_path) as video:
        for i, clip in enumerate(clips, 1):
            start = timestamp_to_seconds(clip['start'])
            end = timestamp_to_seconds(clip['end'])
            new_clip = video.subclipped(start, end)
            new_clip.write_videofile(f"{output_dir}/short_{i}.mp4", codec="libx264", logger=None)
    return output_dir