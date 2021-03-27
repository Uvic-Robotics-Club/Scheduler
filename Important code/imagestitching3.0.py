#imagestitching3.0.py
#from imutils import paths
import numpy as np
import argparse
#import imutils
import cv2


#ausdom webcam
videofeed=cv2.VideoCapture(2)
#2 is main webcam avermedia 
#maybe it changes? 
imagesToBeStitched=[]
counter=0
while counter <300:
    _, imageframe=videofeed.read()
    print(counter)
    if (counter%10)==0:
        
        imagesToBeStitched.append(imageframe)
        
        #creating a list  of every couple frames to then stitch together
        
    counter=counter+1

cv2.imshow("list", imagesToBeStitched[0])
cv2.waitKey(1000)
#cv2.imshow("list", imagesToBeStitched[1])
#cv2.waitKey(0)



#cv2.imshow("list", imagesToBeStitched[2])
print(counter)
stitcher = cv2.Stitcher_create() 

#creating stitcher?

(status,stitched)=stitcher.stitch(imagesToBeStitched)
print("stitch attempt complete ")
#doing the stitching

# if the status is '0', then OpenCV successfully performed image
# stitching
print("number of images ", len(imagesToBeStitched) )
if status == 0:
	# write the output stitched image to disk
	cv2.imwrite("Stitchedimage.png", stitched)
	# display the output stitched image to our screen
	cv2.imshow("Stitched", stitched)
	cv2.waitKey(10000)
    #waitkey dispalys image for a certain amount of time in milliseconds
    #so 1 second is 1000ms 
# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
	print("image stitching failed ({})".format(status))

