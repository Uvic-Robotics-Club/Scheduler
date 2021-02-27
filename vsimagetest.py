import cv2 as cv

img= cv.imread("images.jpg")
#he says u can input path relatively if its in working directory, 
#can provide absolute paths if not 

cv.imshow('test', img)
cv.waitKey(0)
#^waits forever for a key to be pressed