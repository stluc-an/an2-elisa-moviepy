import moviepy.video.compositing
from moviepy.editor import *

clip: object = VideoFileClip("Legend.mp4").subclip(50, 60)
txt_clip = TextClip("CA MARCHE", fontsize=70, color='white')
txt_clip = txt_clip.set_pos('center').set_duration(30)

video = CompositeVideoClip([clip, txt_clip])
video.write_videofile("Legend_test.mp4")
