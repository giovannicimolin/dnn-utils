import numpy as np
import os
import glob
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util


if tf.__version__ != '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.0!')

#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

for image_type in ['rgb', 'gvi', 'vvi']:
    print("Loading model {}...".format(image_type))
    MODEL_NAME = 's3/{}/ssd_inception_v2_coco'.format(image_type)
    PATH_TO_CKPT = MODEL_NAME + '/inference_graph/frozen_inference_graph.pb'
    SAVE_IMAGES_PATH = MODEL_NAME + '/map'
    PATH_TO_LABELS = os.path.join('data', 'objects.pbtxt')
    NUM_CLASSES = 1

    print("Loading model from: {}".format(PATH_TO_CKPT))
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    def load_image_into_numpy_array(image):
      (im_width, im_height) = image.size
      return np.array(image.getdata()).reshape(
          (im_height, im_width, 3)).astype(np.uint8)

    PATH_TO_TEST_IMAGES_DIR = 'map'
    TEST_IMAGE_PATHS = list(glob.iglob('{}/*'.format(PATH_TO_TEST_IMAGES_DIR)))
    print("Found {} images...".format(len(TEST_IMAGE_PATHS)))
    print(SAVE_IMAGES_PATH)

    try:
        os.makedirs(SAVE_IMAGES_PATH)
    except:
        pass

    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        data = []
        for image_path in TEST_IMAGE_PATHS:
          image = Image.open(image_path)
          # the array based representation of the image will be used later in order to prepare the
          # result image with boxes and labels on it.
          image_np = load_image_into_numpy_array(image)
          # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
          image_np_expanded = np.expand_dims(image_np, axis=0)
          # benchmark
          start = time.time()
          # Actual detection.
          (boxes, scores, classes, num) = sess.run(
              [detection_boxes, detection_scores, detection_classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
          # benchmark
          end = time.time()
          elapsed = end - start
          # Visualization of the results of a detection.
          print("Processing image: {} - {}...".format(image_type, image_path))
          vis_util.visualize_boxes_and_labels_on_image_array(
              image_np,
              np.squeeze(boxes),
              np.squeeze(classes).astype(np.int32),
              np.squeeze(scores),
              category_index,
              max_boxes_to_draw=100,
              use_normalized_coordinates=True,
              line_thickness=2)

          im = Image.fromarray(image_np)
          im.save(MODEL_NAME+'/'+image_path)
          for box in np.squeeze(boxes):
              data.append({
                'filename':  image_path.split('/')[-1],
                'xmin': int(box[0]*512),
                'ymin': int(box[1]*512),
                'xmax': int(box[2]*512),
                'ymax': int(box[3]*512),
                'time': elapsed,
              })

        print("Saving box info file...")
        import csv

        keys = data[0].keys()
        with open("{}/boxes.csv".format(SAVE_IMAGES_PATH), 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
