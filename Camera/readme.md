
# Video Camera 

Grab the webcam data in pieces that can be transmitted over the network

## Open CV module and python version 

```
python version 3.8.1
opencv version 4.1.2.30
```

## Installing 
```
pip3 install opencv-python==4.1.2.30
```
This is the not the latest version of opencv, as the latest one somehow crashes when using the VideoFeed file.

## Documentation 

For opencv module 

'''
https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
'''

## How it works

There are two methods of encoding/decoding and both methods will work.
opencv has its own built in encoding/decoding.
There is also a built in python module called pickle that will encode it in bytes.