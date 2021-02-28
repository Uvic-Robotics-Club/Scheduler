import cv2 as cv
import numpy as np
from cv2 import aruco 

#define Aruco Dictionary
dictionary = aruco.Dictionary_get(cv.aruco.DICT_5X5_250)

#set up blank matrix 
markerImg = np.zeros((100,100))

#draw marker on blank matrix
markerImg = aruco.drawMarker(dictionary,13,50, markerImg, 1)

#save marker
cv.imwrite("marker13.png",markerImg)

 
