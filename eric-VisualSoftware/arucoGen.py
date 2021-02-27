import cv2 as cv
import numpy as np

dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_250)

markerImg = np.zeros((200,200),dtype="uint8")
markerImg = cv.aruco.drawMarker(dictionary,13,200, markerImg, 1)

cv.imwrite("marker33.png",markerImg)

 
