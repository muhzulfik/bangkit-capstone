# Bangkit-Capstone

## This is progress from "hoper mor"'s capstone project
Firstly, let us introduce our team. Our team called "hoper mor". Precipitating "hoper mor" because we create applications that will be devoted to mothers and baby for the prevention of stunting.
This project is intended to prevent stunting early, which starts from pregnant mothers to babies under 2 years.
This repository for cloud computing and machine learning path of our team, for android path have different repository because they need more space, so, here we go.
Our team choose yolov3 for model machine learning because it can detection more than 1 object so makes it easier for us to process data in the cloud and also makes it easier for users without having to take pictures repeatedly.
In 2020, the percentage of children under five with stunting in Indonesia will reach 11.6% of the target of 24.1%. while the standard of who is 20%, we want to help reduce the percentage even smaller, so, here we go, we hope this application can help families who are less fortunate because of our thinking, the correlation between people with stunting and the economic conditions of the family is quite large. Where the higher the economic income of the family, lower the probability of suffering from stunting.

#CLOUD COMPUTING
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
