import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from sklearn.cluster import KMeans

print("Loading...")

img = cv2.imread('hawaii.jpg', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
data = img.reshape((-1,3))
data = np.float32(data)

# TERM_CRITERIA_EPS : iteration stops if specified accuracy, epsilon, is reached
# TERM_CRITERIA_MAX_ITER : stops after the specified number of iterations, max_iter
# max_iter : 10
# epsilon : 1.0
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
output = []
titles = []

output.append(img)
titles.append('Original Image')

def onChanged_trackbar(x):
    # get current positions of trackbars
    K_i = cv2.getTrackbarPos('K','Original Image')
    if K_i != 0:
        newOutput = CalculateKMeans(K_i)
        newOutput = cv2.cvtColor(newOutput, cv2.COLOR_BGR2RGB)
        cv2.imshow('Original Image', newOutput)
    else:
        newOutput = np.zeros([540, 960, 3], np.uint8)
        alertStr = 'No clustering for K=0'
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(newOutput, alertStr, (150, 270), font, 2, (255, 255, 255), 2)
        cv2.imshow('Original Image', newOutput)
    return

def CalculateKMeans(K_i):
    compactness, labels, centers = cv2.kmeans(data, K_i, None,
                                    criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    newOutput = res.reshape((img.shape))
    return newOutput

def onclick_select(event):
    for i in range(9):
        if event.inaxes == subplots[i]:
            newImage = cv2.cvtColor(output[i], cv2.COLOR_BGR2RGB)
            if i == 0:
                cv2.namedWindow('Original Image')
                cv2.createTrackbar('K', 'Original Image', 0, 30, onChanged_trackbar)
                cv2.imshow('Original Image', newImage)
            else:
                cv2.imshow('K = ' + str(i+2), newImage)
            return

for i in range(3, 11):
    K = i
    # 10 : number of times the algorithm is executed using different initial labellings
    # KMEANS_RANDOM_CENTERS : random set of initial samples, and tries to converge
    # KMEANS_PP_CENTERS : first iterates the whole image to determine the probable
    #                     centers and then starts to converge
    # compactness : sum of squared distance
    # labels : label array where each element marked '0', '1', ...
    # centers : array of centers of clusters
    compactness, labels, centers = cv2.kmeans(data, K, None,
                                    criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    output.append(res.reshape((img.shape)))
    titles.append('K=' + str(K))

print("Completed\n")
    
subplots = []

# remove default navigation
matplotlib.rcParams['toolbar'] = 'None'

# create window with title
fig = plt.figure(num='MAT345_taehoon.kwon_project4')
fig.suptitle(t = 'Click on each picture to view it in a new window\n'
    + 'Original Image has a slide bar to update image from k=1 to k=30', y = 0.95)

for i in range(9):
    # make sub plot and show with each titles
    subplots.append(fig.add_subplot(3, 3, i+1))
    plt.imshow(output[i])
    plt.title(titles[i])

    # remove axis ticks
    plt.xticks([])
    plt.yticks([])
plt.subplots_adjust(bottom = 0.05, top = 0.85)
fig.canvas.mpl_connect("button_press_event",onclick_select)

#----------------------------------------------------------------
# The code below is the distortion line graph using elbow method.
# Algorithm is too slow, so uncomment only when you want to check
#----------------------------------------------------------------
#pltfig = plt.figure(num='MAT345_taehoon.kwon_Elbow_Method')
## calculate distortion for a range of number of cluster
#distortions = []
#for i in range(1, 11):
#    km = KMeans(
#        n_clusters=i, init='random',
#        n_init=10, max_iter=10,
#        tol=1.0, random_state=0
#    )
#    km.fit(data)
#    distortions.append(km.inertia_)
#
## plot
#plt.plot(range(1, 11), distortions, marker='o')
#plt.xlabel('Number of clusters')
#plt.ylabel('Distortion')

plt.show()