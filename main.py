from flask import Flask, request, jsonify
import os
import pymysql
from flaskext.mysql import MySQL
import time
from absl import app
import tensorflow as tf
from yolov3.models import YoloV3

classes_data = './labels/food.names'
model_path = './model/yolov3_fix.tf'
size = 416
datasets = 7                # number of datasets in your model

yolo = YoloV3(classes=datasets)
yolo.load_weights(model_path).expect_partial()
class_names = [
    x.strip()
    for x in open(classes_data).readlines()
    ]

app = Flask(__name__)

# config mysql
mysql = MySQL()
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'HaperMor'
app.config['MYSQL_DATABASE_DB'] = 'task'
app.config['MYSQL_DATABASE_HOST'] = '34.101.85.165'
mysql.init_app(app)

def convert_img(img_train, size):
    img_train = tf.image.resize(img_train, (size, size))
    img_train = img_train / 255
    return img_train

resp = []

@app.route('/detect', methods=['POST', 'GET'])
def get_img():
    raw_img = []
    img = request.files.getlist("images")
    img_names = []
    for image in img:
        image_name = image.filename
        img_names.append(image_name)
        image.save(os.path.join(os.getcwd(), image_name))
        img_raw = tf.image.decode_image(
            open(image_name, 'rb').read(), channels=3)
        raw_img.append(img_raw)
        
    amount_data = 0
    response_json = []

    for data_img in range(len(raw_img)):
        global resp
        resp = []
        raw_img = raw_img[data_img]
        amount_data+=1
        img = tf.expand_dims(raw_img, 0)
        img = convert_img(img, size)

        boxes, scores, classes, nums = yolo(img)
        
        for i in range(nums[0]):
            resp.append({
                "class": class_names[int(classes[0][i])]
            })
        response_json.append({
            "detections": resp
        })
    
    for name in img_names:
        os.remove(name)

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    foods = []
    for i in resp:
        cur.execute('SELECT * FROM makanan WHERE nama_makanan="{}";'.format(i['class']))
        exc = cur.fetchall()
        if(len(exc) > 0):
            food = exc[0]
            cur.execute('SELECT * FROM nutrisi WHERE id_makanan={};'.format(food["id_makanan"]))
            ukuran = cur.fetchall()
            food['ukuran'] = ukuran
            foods.append(food)

    return jsonify(foods)

@app.route('/resep', methods=['GET'])
def resep():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('''SELECT * FROM resep;''')

    exc = cur.fetchall()

    return jsonify(exc)

if __name__ == '__main__':
    app.run(debug=True)
