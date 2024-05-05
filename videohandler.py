import moviepy.editor as mp
import os
def video_handler(video_note: str) -> None:
    clip = mp.VideoFileClip(video_note)
    clip.audio.write_audiofile("voice.wav")
    os.remove(video_note)
