#!/usr/bin/python
import time
import cv2
import socket
import numpy as np
import os
import sys
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util
from imutils.video import VideoStream
import imutils

#sys.stdout = open("/home/pi/error.log","a")

print("Done Importing")
#print("Starting Download...")

# What model to download.
MODEL_NAME = 'redcircle_inference_graph'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + "/frozen_inference_graph.pb" 

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('training', 'object-detection.pbtxt')

NUM_CLASSES = 1

# Download Model
#opener = urllib.request.URLopener()
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#tar_file = tarfile.open(MODEL_FILE)
#for file in tar_file.getmembers():
#   file_name = os.path.basename(file.name)
#    if 'frozen_inference_graph.pb' in file_name:
#        tar_file.extract(file, os.getcwd())
#print("Model has been downloaded")

# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
print("Model Loaded into tensor flow")

# Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
print("Loaded label map model")

# Helper code
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

# Size, in inches, of the output images.
IMAGE_SIZE = (640, 480)

# Connect to main
client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 8080))
#client_socket.send(b"PiCam,0,0")

#connection = client_socket.makefile('wb')
usingPiCamera = True
# Set initial frame size.
frameSize = (320, 240)

try:

    cap = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=frameSize,framerate=32).start()
    # allow the camera to warmup
    num = 0
    time.sleep(2)
    print("Camera on")
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while True:
                image_np = cap.read()
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
		print("Starting Classification")
		(boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded}
                )
		print("Done Classifing")
                
                # Send robot ready if first classification is done
                if num != 1:
                    num = 1
                    client_socket.send(b'PiCam,Robot Ready,0')

                image_np.setflags(write=1)
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array (
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8,
                )
		#print(category_index)
                #print(classes)
                print(scores)
                #print(boxes)
                #print(category_index[classes[0][1]]['name'])
		if(scores[0][0] > 0.8 and classes[0][0] == 1):
		    midline = (boxes[0][0][3] +  boxes[0][0][1]) / 2
		    padding = 0.1
		    if midline > (0.5 + padding):
                        data = 'PiCam,TurnRight,' + str(midline)
                        print(data)
		        client_socket.send(data)
                        time.sleep(0.01)
		    if midline < (0.5 - padding):
                        data = 'PiCam,TurnLeft,' + str(midline)
                        print(data)
		        client_socket.send(data)
                        time.sleep(0.01)
		    else:
                        client_socket.send(b'PiCam,RoboInFront,0')
                        time.sleep(0.01)
		
		if (cv2.waitKey(25) & 0xFF == ord('q')): break
finally:
    print("done...")
    cap.stop()
    sys.stdout = sys.__stdout__
    client_socket.send(b'\n')
    client_socket.close()
