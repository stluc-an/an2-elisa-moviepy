import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
import time
import colorsys

from moviepy.editor import *
from moviepy.video.tools.cuts import *
def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

#print(time.time())
clip = VideoFileClip("input/red.mp4")
clip = clip.resize(width=60)
print(clip.duration,clip.fps)
print(clip.duration * clip.fps)
imgLen = int(clip.duration * clip.fps)
old_hue_avg = 0
scene_start = 0

hue_threshold = 0.15


scenes = []

for x in np.linspace(0,clip.duration,clip.duration*2):
#for x in range(1, imgLen):
    #try:
    img = clip.get_frame(x)#x c'est en secondes
    imgok = img
    #ImageClip(x).save_frame("color_img.jpg")
    cv2.imwrite('color_img2.jpg', img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number

    clt = KMeans(n_clusters=4) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)

    colors = [colorsys.rgb_to_hsv(c[0],c[1],c[2]) for c in clt.cluster_centers_ / 255 ]


    hues = [c[0] for c in colors]
    ##print(hues)
    if len(hist) != 1:
        hue_avg = np.average(hues,weights = hist, axis=None)
        hue_deviation = np.std(hues)
        ##print(hues)
        print(x, old_hue_avg - hue_avg, hue_deviation)

        # changement de scène?
        if abs(old_hue_avg - hue_avg) > hue_threshold :
            print("CHANGEMENT DE SCENEç!!!!!")
            scenes.append([(scene_start, x), hue_avg, hue_deviation])
            scene_start = x

        old_hue_avg = hue_avg

    else:
        print("Black?")
        #cv2.imwrite('black '+ str(x) +'.jpg', imgok)
        ##print(hue_deviation)

        #print(time.time())
        ##bar = plot_colors2(hist, clt.cluster_centers_)

        ##plt.axis("off")
        ##plt.imshow(bar)
        ##plt.show()
    #except TypeError as e:
        #print(e)
        #print(x/clip.fps, "black")

print(scenes)

for scene in scenes:
    sceneClip = clip.subclip(scene[0][0], scene[0][1])
    sceneClip.write_videofile("los/los " + str(scene[1]) + ".mp4")