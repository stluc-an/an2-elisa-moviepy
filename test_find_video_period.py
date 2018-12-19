from moviepy.editor import *
from moviepy.video.tools.cuts import *

clip = VideoFileClip("ar.mp4")

result = detect_scenes(clip, thr=30)
scenes = result[0]


