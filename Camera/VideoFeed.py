import cv2
import pickle
from datetime import datetime 
from scheduler_types import *
import scheduler
import workAdder
import threading
import queue
from time import sleep, time


# Queue that both main thread and scheduler threads share
qVideo = queue.Queue()

# Producer
class VideoFeed:
    def __init__(self, maxPollRateSeconds, maxInQueue=10):
        # The maximum poll rate of the object. Set to '0' for unlimited (note: this is still capped by main code)
        self.pollRate = maxPollRateSeconds
        # Will store the last time the object has been polled. Used in logic to control rate
        self.time = time()
        # Limits how many of this object's event functions can be in the queue at the same time.
        # Most commonly will be 1 for objects that get data in the event function (most recent data),
        # or about 10 for functions that record data when polled (need every instance to be processed in order)
        self.maxInQueue = maxInQueue
        # Stores current number in queue
        self.inQueueCount = 0
        # Tracks all functions that should be called when an event happens
        self.functs = []
        # 3 is the average priority. Lower priorities go first.
        self.priority = 1

        self.cap = cv2.VideoCapture(0)  # This will be changed to an integer later for the camera
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    # Add this function to Scheduler's poll list. For consistency, do not rename.
    def poll_function(self):
        if time() - self.time > self.pollRate and self.inQueueCount < self.maxInQueue:
            # Update internal time to when it was most recently added to the queue
            self.time = time()

            # -------------   Optional: ADD CODE HERE   -------------
            # DO NOT add any code that takes a significant amount of time here.
            # DO NOT add anything that can block!

            self.inQueueCount += 1
            return [Pq_obj(self.priority, self.event_function)]



    # When poll function determines something should happen, this is where it actually happens
    # It's okay to take a bit of time here, but do not block.
    def event_function(self):

        # Code Josh put: a bit redundant (encoding it then decoding but rough draft to run in local system)
        frame = self.stream()
        encoded, buffer = self.encode_cv(frame)
        decoded_frames = self.decode_cv(buffer)

        # Run all the functions that are supposed to run on an event.
        doLater = []
        if self.functs:
            for f in self.functs:
                res = f(buffer)
                # Track anything we need to process later
                if res is not None:
                    doLater.append(res)

        # Note: track when finished, not when started, so we can't spawn too many if the function
        # takes a lot of time
        self.inQueueCount -= 1
        if len(doLater) > 0:
            return doLater

    # Provides a way to link functions from other objects to events from this producer.
    # Note: it is the consumer's responsibility to
    def add_function_to_call(self, function):
        self.functs.append(function)

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

# Consumer
class OutputFeed:

    def decode_cv(self,frame):
        source = cv2.imdecode(frame, 1)
        return source

    def on_event(self,buffer):
        decoded_frames = self.decode_cv(buffer)
        qVideo.put(decoded_frames)


def main():
    # Initialize list of functions to poll

    functs = []

    video = VideoFeed(0,1)  # Producer

    output = OutputFeed()  # Consumer
    video.add_function_to_call(output.on_event)

    functs.append(video.poll_function)

    s = scheduler.Scheduler(8, functs)
    wA = workAdder.workAdder(s)
    s.run()
    wA.add_pq_obj(Pq_obj(3, stupid_print))



    while True:

        decoded_frames = qVideo.get()
        image = cv2.flip(decoded_frames,1)
        cv2.imshow('Window', image)

        c = cv2.waitKey(1)
        if c == 27: #key 27 is esc
            break
    s.stop()
    video.cap.release()
    cv2.destroyAllWindows()


def stupid_print():
    print("Here's your print statement, stupid")


if __name__ == "__main__":
    main()