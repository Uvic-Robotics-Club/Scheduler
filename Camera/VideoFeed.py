import cv2
import pickle

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

    # These two functions use pickle module
    # encodes frames into bytes
    def encode_pickle(self,frame):
        data = pickle.dumps(frame)
        return data

    # decodes the bytes back into frames
    def decode_pickle(self,frame):
        data = pickle.loads(frame)
        return data

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
        
        cv2.imshow('Window', decoded_frames)

        c = cv2.waitKey(1)
        if c == 27: #key 27 is esc
            break

    camera_feed.cap.release()
    cv2.destroyAllWindows()

main()