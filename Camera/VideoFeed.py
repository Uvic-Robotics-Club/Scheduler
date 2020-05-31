import cv2
import pickle
from datetime import datetime 

class VideoFeed(object):

    def __init__(self):
        self.cap = cv2.VideoCapture(0) #This will be changed to an integer later for the camera
        
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    # Returns the frames of the feed
    def stream(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) # Resizing the frames
        return frame

    # These two functions use opencv module
    def encode_cv(self,frame):
        encoded, buffer = cv2.imencode('.jpg', frame)
        return encoded, buffer

    def decode_cv(self,frame):
        source = cv2.imdecode(frame, 1)
        return source


def main():
    camera_feed = VideoFeed()
    while True:
        frame = camera_feed.stream()

        encoded, buffer = camera_feed.encode_cv(frame)

        decoded_frames = camera_feed.decode_cv(buffer)

        image = cv2.flip(decoded_frames,1)
        cv2.imshow('Window', image)

        c = cv2.waitKey(1)
        if c == 27: #key 27 is esc
            break
        elif c == 32: # Space, takes picture
            now = datetime.now()
            img_name = "cv_image_{}.png".format(str(now.minute)+"-"+str(now.second)+"-"+str(now.day))
            cv2.imwrite(img_name,frame)
    
    camera_feed.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()