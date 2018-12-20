import time
from colour_analysis import *

from moviepy.editor import *
from moviepy.video.tools.cuts import *

from operator import itemgetter, attrgetter

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

# variables fichiers/chemins
vid_path = "input/"
vid_file = "los.mp4"
output_path = "output/"

# variables analyse de couleur
hue_threshold = 0.15
nb_clusters = 4
video_resize = 64 #on fait l'analyse sur une video réduite!
processing_fps = 4 #on fait l'analyse sur x frames par seconde

# charger et resizer le film
clip_original = VideoFileClip(vid_path + vid_file)
clip = clip_original.resize(width=video_resize)
imgLen = int(clip.duration * clip.fps)

# variables utilisées durant l'analyse et la découpe
prev_hue_avg = -1
prev_time = 0
scene_nb = 0
scene_start = 0

scenes = []

# on parcourt les images et on analyse
for x in np.linspace(0, clip.duration, clip.duration * processing_fps):
    # récupère la frame à x secondes
    img = clip.get_frame(x)

    clusters = get_clusters(img, nb_clusters)

    hist = find_histogram(clusters, nb_clusters)
    hues = get_hues(clusters)

    print("hist", hist)
    print("hues", hues)

    hue_avg = np.average(hues, weights=hist, axis=None)

    hue_deviation = np.std(hues)

    print(x, prev_hue_avg - hue_avg, hue_deviation)

    # changement de scène?
    if abs(prev_hue_avg - hue_avg) > hue_threshold and prev_hue_avg != -1:
        print("Scene",scene_nb)
        print("Average hue",prev_hue_avg)
        print("Hue derivation", hue_deviation)
        scenes.append([(scene_start, prev_time), prev_hue_avg, hue_deviation])
        scene_start = x
        scene_nb += 1

    #dernière scène
    if x == clip.duration:
        print("Last scene")
        scenes.append([(scene_start, x), prev_hue_avg, hue_deviation])

    # mise à jour pour le prochain passage dans l'itération
    prev_hue_avg = hue_avg
    prev_time = x


print(scenes)

# on sauve la liste dans un fichier, pour récupérer la liste des scènes plus tard
with open(vid_path + vid_file + ".pkl", "wb") as fexport:
    pickle.dump(scenes, fexport)

# pour lire la liste des scènes:
#with open(vid_path + vid_file + ".pkl", "rb") as fimport:
#    clips = pickle.load(fimport)

# on trie les scenes par hue puis par uniformité ;)
scenes = sorted(scenes,key=itemgetter(1,2))

# on va parcourir le tableau des scènes et exporter les bouts de vidéos
i = 1

for scene in scenes:
    sceneClip = clip_original.subclip(scene[0][0], scene[0][1])
    try:
        sceneClip.write_videofile(output_path + vid_file + format(i, "05d") + ".mp4")
    except Exception as e:
        print ("Erreur pendant export",e)
    i += 1
