import tensorflow as tf
import numpy as np
import cv2

# fit the image with the model size
def resize_the_image(input, size_of_model):
    input= tf.image.resize(input, size_of_model)
    return input

def load_the_class_names(file_name):
    with open(file_name, 'r') as f:
        class_names = f.read().splitlines()
    return class_names

def non_max_suppression(input, model_size, maxi_output_size, maxi_output_size_per_class, iou_threshold, confidence_threshold):
    box, confs, class_prob = tf.split(input, [4, 1, -1], axis=-1)
    box=box/model_size[0]
    scores = confs * class_prob
    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(box, (tf.shape(box)[0], -1, 1, 4)),
        scores=tf.reshape(scores, (tf.shape(scores)[0], -1, tf.shape(scores)[-1])),
        maxi_output_size_per_class=maxi_output_size_per_class,
        maxi_total_size=maxi_output_size,
        iou_threshold=iou_threshold,
        score_threshold=confidence_threshold
    )
    return boxes, scores, classes, valid_detections

#making boxes dicts
def output_boxes(input,model_size, maxi_output_size, maxi_output_size_per_class,
                 iou_threshold, confidence_threshold):
    x_center, y_center, width, height, confidence, classes = \
        tf.split(input, [1, 1, 1, 1, 1, -1], axis=-1)
    x_top_left = x_center - width / 2.0
    y_top_left = y_center - height / 2.0
    x_bottom_right = x_center + width / 2.0
    y_bottom_right = y_center + height / 2.0
    input = tf.concat([x_top_left, y_top_left, x_bottom_right,
                        y_bottom_right, confidence, classes], axis=-1)
    boxes_dicts = non_max_suppression(input, model_size, maxi_output_size,
                                      maxi_output_size_per_class, iou_threshold, confidence_threshold)
    return boxes_dicts

#draw the box of output detection
def draw_outputs(img, boxes, objectness, classes, nums, class_names):
    boxes, objectness, classes, nums = boxes[0], objectness[0], classes[0], nums[0]
    boxes=np.array(boxes)
    for i in range(nums):
        x1y1 = tuple((boxes[i,0:2] * [img.shape[1],img.shape[0]]).astype(np.int32))
        x2y2 = tuple((boxes[i,2:4] * [img.shape[1],img.shape[0]]).astype(np.int32))
        img = cv2.rectangle(img, (x1y1), (x2y2), (255,0,0), 2)
        img = cv2.putText(img, '{} {:.4f}'.format(
            class_names[int(classes[i])], objectness[i]),
                          (x1y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        return img
