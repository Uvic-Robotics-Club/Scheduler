import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randrange

image1=cv2.imread('Rightimage.JPG')
image1colour=cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#The cv2.cvtColor converts the input RGB image into its grayscale form.

image2=cv2.imread('Leftimage.JPG')
image2colour=cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)

#For image stitching, we have the following major steps to follow:
##1 Compute the sift-keypoints and descriptors for both the images.
#2 Compute distances between every descriptor in one image and every descriptor in the other image.
#3 Select the top ‘m’ matches for each descriptor of an image.
#4 Run RANSAC to estimate homography
#5 Warp to align for stitching
#6 Now stitch them together

sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(image1,None)
kp2, des2 = sift.detectAndCompute(image2,None)

'''
kp1 and kp2 are keypoints, des1 and des2 are the descriptors of the respective images.
Now, the obtained descriptors in one image are to be recognized in the image too. We do that as follows:
'''

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
'''
The BFMatcher() matches the features which are more similar. 
When we set parameter k=2, we are asking the knnMatcher to give out 2 best matches for each descriptor.
Often in images, there are tremendous chances where the features may be existing in many places of the image. 
This may mislead us to use trivial features for our experiment. So we filter out through all the matches to 
obtain the best ones. So we apply ratio test using the top 2 matches obtained above. We consider a match if the 
ratio defined below is predominantly greater than the specified ratio.'''

# Apply ratio test
good = []
for m in matches:
    if m[0].distance < 0.5*m[1].distance:
        good.append(m)
    matches = np.asarray(good)
print(len(matches))
if len(matches[:,0]) >= 4:
    src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
    dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
    H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    #print H
else:
    raise AssertionError('Can’t find enough keypoints.')


dst = cv2.warpPerspective(image1,H,(image2.shape[1] + image1.shape[1], image2.shape[0]))
plt.subplot(122),plt.imshow(dst),plt.title('Warped Image')
plt.show()
plt.figure()
dst[0:image2.shape[0], 0:image2.shape[1]] = image2
cv2.imwrite('output.jpg',dst)
plt.imshow(dst)
plt.show()