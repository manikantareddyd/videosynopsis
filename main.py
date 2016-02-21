import tensorflow as tf
import numpy as np
import cv2

def get_frames(vpath,resize_ratio):
    cap = cv2.VideoCapture(vpath)

    if not cap.isOpened():
        print "could not open : ",vpath
        return

    length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    width  = int(int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))*resize_ratio)
    height = int(int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))*resize_ratio)
    fps    = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    print "Number of input frames: ",length
    print "Width: " ,width
    print "Height: " ,height
    print "Frames per second: ", fps

    frames = np.zeros((length,height*width, 3), dtype=np.uint8)

    for i in range(0,length+1):
        try:
            ret,frame = cap.read()
            # print ret,frame
            rframe = cv2.resize(frame,None,fx=resize_ratio,fy=resize_ratio, interpolation=cv2.INTER_CUBIC)
            # print rframe.shape
            frames[i] = np.resize(rframe,(height*width,3))
        except Exception as e:
            print "Cannot read video file", e
            break

    return frames

fs = get_frames("data/input_video_sample1.mov",0.25)
print fs.shape,fs
