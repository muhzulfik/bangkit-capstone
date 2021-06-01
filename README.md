# bangkit-capstone

# Install requirements
pip install -r requirements.txt

# Saving your yolov3 weights as a TensorFlow model.
python weights_to_tf.py

#run the Flask app on port 5000.
python app.py

# custom your weights and classes in main.py
classes_data = './labels/food.names'
model_path = './model/yolov3_fix.tf'
size = 416
datasets = 7                # number of classes in model

# Google Cloud Platform
- create database server using Cloud SQL
- deploy flask app in VM/cloud computing

