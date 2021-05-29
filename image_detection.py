import tensorflow as tf
from make_box import load_the_class_names, output_boxes, draw_outputs, resize_the_image
from yolov3 import YOLOv3Net
import numpy as np
import cv2


class_name = './data/coco.names'
num_classes = 7
model_size = (416, 416,3)
maxi_output_size = 40
maxi_output_size_per_class= 20
iou_threshold = 0.5
confidence_threshold = 0.5

cfgfile = 'cfg/yolov3.cfg'
weightfile = 'weights/yolov3_weights.tf'
img_path = "img/telur rebus1.jpg"
physic_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physic_devices) > 0, "Not enough GPU hardware devices available"
tf.config.experimental.set_memory_growth(physic_devices[0], True)


def main():
    model = YOLOv3Net(cfgfile,model_size,num_classes)
    model.load_weights(weightfile)
    class_names = load_the_class_names(class_name)
    image = cv2.imread(img_path)
    image = np.array(image)
    image = tf.expand_dims(image, 0)
    resized_frame = resize_the_image(image, (model_size[0],model_size[1]))
    pred = model.predict(resized_frame)
    boxes, scores, classes, nums = output_boxes( \
        pred, model_size,
        maxi_output_size=maxi_output_size,
        maxi_output_size_per_class=maxi_output_size_per_class,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold)
    image = np.squeeze(image)
    img = draw_outputs(image, boxes, scores, classes, nums, class_names)
    win_name = 'Image detection'
    cv2.imshow(win_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('telur rebus1.jpg', img)  #to save the result

if __name__ == '__main__':
    main()