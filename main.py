import tensorflow as tf
import numpy as np
import cv2

tf.app.flags.DEFINE_string("logdir","logs","Directory for saving the logs of computation")
tf.app.flags.DEFINE_string("vpath","","Path of the video to be processed")
tf.app.flags.DEFINE_float("resize_ratio",1.0,"Ratio by which each frame should be resized to reduce memory usage")
tf.app.flags.DEFINE_integer("output_frames",100,"Number of frames in the synopsis video")

FLAGS = tf.app.flags.FLAGS

def get_frames(vpath,resize_ratio):
    vpath = FLAGS.vpath

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

    for i in range(0,length):
        ret,frame = cap.read()
        try:
            # print ret,frame
            if not ret:
                rframe = cv2.resize(frame,None,fx=resize_ratio,fy=resize_ratio, interpolation=cv2.INTER_CUBIC)
                # print rframe.shape
                frames[i] = np.resize(rframe,(height*width,3))
        except Exception as e:
            print "Cannot read video file", e
            # print i,ret
            break

    return frames

def video_synopsis(vpath,resize_ratio,output_frames):

    graph = tf.Graph()

    with graph.as_default():

        with tf.name_scope("input") as scope:
            # video_path = tf.constant(vpath)
            video_path = tf.constant(0,name="video_path") #commented cause tf.string is not supported yet
            rRatio = tf.constant(resize_ratio, dtype=tf.float32,name="resize_ratio")
            k = tf.constant(output_frames, dtype=tf.uint8,name="output_frames")

        with tf.name_scope("video_processing") as scope:
            frames = tf.py_func(get_frames,[video_path,rRatio],[tf.uint8],name="get_frames")[0]

        sess = tf.Session()
        writer = tf.train.SummaryWriter(FLAGS.logdir,sess.graph_def)

        fs = sess.run(frames)

        return fs

fs = video_synopsis(FLAGS.vpath,FLAGS.resize_ratio,FLAGS.output_frames)
print fs.shape
