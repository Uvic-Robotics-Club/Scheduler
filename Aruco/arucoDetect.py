import cv2 as cv
from cv2 import aruco

#start video
cap = cv.VideoCapture(0,cv.CAP_DSHOW)

while(True):
    
    #read each frame
    true, frame = cap.read()
    
    # make a grayscale frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # define Aruco Dictionary
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

    #initialize parameters
    arucoParameters = aruco.DetectorParameters_create()
    
    #detect marker by passing in grayscale frame
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
    
    #draw marker positon and ID on frame
    frame = aruco.drawDetectedMarkers(frame, corners, ids)

    # display frame
    cv.imshow('Display', frame)

    # press d to end loop and terminate arucoDetect.py
    if cv.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv.destroyAllWindows()