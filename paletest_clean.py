import time
from colour_analysis import *

from moviepy.editor import *
from moviepy.video.tools.cuts import *


#print(time.time())
clip = VideoFileClip("input/red.mp4")
clip = clip.resize(width=60)

print(clip.duration,clip.fps)
print(clip.duration * clip.fps)
imgLen = int(clip.duration * clip.fps)
old_hue_avg = 0
scene_start = 0

hue_threshold = 0.15
nb_clusters = 4

scenes = []

for x in np.linspace(0,clip.duration,clip.duration*2):
    #récupère la frame à x secondes
    img = clip.get_frame(x)

    clusters = get_clusters(img,nb_clusters)

    hist = find_histogram(clusters,nb_clusters)
    hues = get_hues(clusters)

    print ("hist",hist)
    print ("hues",hues)

    hue_avg = np.average(hues,weights = hist, axis=None)
    hue_deviation = np.std(hues)
    
    print(x, old_hue_avg - hue_avg, hue_deviation)

    # changement de scène?
    if abs(old_hue_avg - hue_avg) > hue_threshold :
        print("CHANGEMENT DE SCENEç!!!!!")
        scenes.append([(scene_start, x), hue_avg, hue_deviation])
        scene_start = x

    old_hue_avg = hue_avg


print(scenes)

for scene in scenes:
    sceneClip = clip.subclip(scene[0][0], scene[0][1])
    sceneClip.write_videofile("los/los " + str(scene[1]) + ".mp4")