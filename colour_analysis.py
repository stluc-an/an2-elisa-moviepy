import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
import cv2
import numpy as np
import colorsys

def find_histogram(clt,nc):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    #numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    #(hist, _) = np.histogram(clt.labels_, bins=numLabels)
    (hist, _) = np.histogram(clt.labels_, bins=nc)

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

def get_clusters(img, nc):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1], 3))  # represent as row*column,channel number

    clt = KMeans(n_clusters=nc)  # cluster number
    clt.fit(img)

    return clt

def get_hues(clusters):
    colors = [colorsys.rgb_to_hsv(c[0],c[1],c[2]) for c in clusters.cluster_centers_ / 255 ]

    hues = [c[0] for c in colors]

    return hues