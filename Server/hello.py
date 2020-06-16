from __future__ import division, print_function
from flask import Flask, redirect, url_for, request, render_template, jsonify,make_response
import json
from PIL import Image 
from werkzeug.utils import secure_filename
import numpy as np
from gevent.pywsgi import WSGIServer
import sys
import os
from binascii import a2b_base64
import glob
global model,graph
import tensorflow as tf
from base64 import decodestring

app = Flask(__name__)

classes = ['Apple Braebun',
'Apple Crimson Snow',
'Apple Golden 1',
'Apple Golden 2',
'Apple Golden 3',
'Apple Granny Smith',
'Apple Pink Lady',
'Apple Red 1',
'Apple Red 2',
'Apple Red 3',
'Apple Red Delicious',
'Apple Red Yellow 1',
'Apple Red Yellow 2',
'Apricot',
'Avocado',
'Avocado ripe',
'Banana',
'Banana Lady Finger',
'Banana Red',
'Beetroot',
'Blueberry',
'Cactus fruit',
'Cantaloupe 1',
'Cantaloupe 2',
'Carambula',
'Cauliflower',
'Cherry 1',
'Cherry 2',
'Cherry Rainier',
'Cherry Wax Black',
'Cherry Wax Red',
'Cherry Wax Yellow',
'Chestnut',
'Clementine',
'Cocos',
'Corn',
'Corn Husk',
'Cucumber Ripe',
'Cucumber Ripe 2',
'Dates',
'Eggplant',
'Fig',
'Ginger Root',
'Granadilla',
'Grape Blue',
'Grape Pink',
'Grape White',
'Grape White 2',
'Grape White 3',
'Grape White 4',
'Grapefruit Pink',
'Grapefruit White',
'Guava',
'Hazelnut',
'Huckleberry',
'Kaki',
'Kiwi',
'Kohlrabi',
'Kumquats',
'Lemon',
'Lemon Meyer',
'Limes',
'Lychee',
'Mandarine',
'Mango',
'Mango Red',
'Mangostan',
'Maracuja',
'Melon Piel de Sapo',
'Mulberry',
'Nectarine',
'Nectarine Flat',
'Nut Forest',
'Nut Pecan',
'Onion Red',
'Onion Red Peeled',
'Onion White',
'Orange',
'Papaya',
'Passion Fruit',
'Peach',
'Peach 2',
'Peach Flat',
'Pear',
'Pear 2',
'Pear Abate',
'Pear Forelle',
'Pear Kaiser',
'Pear Monster',
'Pear Red',
'Pear Stone',
'Pear Williams',
'Pepino',
'Pepper Green',
'Pepper Orange',
'Pepper Red',
'Pepper Yellow',
'Physalis',
'Physalis with Husk',
'Pineapple',
'Pineapple Mini',
'Pitahaya Red',
'Plum',
'Plum 2',
'Plum 3',
'Pomegranate',
'Pomelo Sweetie',
'Potato Red',
'Potato Red Washed',
'Potato Sweet',
'Potato White',
'Quince',
'Rambutan',
'Raspberry',
'Redcurrant',
'Salak',
'Strawberry',
'Strawberry Wedge',
'Tamarillo',
'Tangelo',
'Tomato 1',
'Tomato 2',
'Tomato 3',
'Tomato 4',
'Tomato Cherry Red',
'Tomato Heart',
'Tomato Maroon',
'Tomato Yellow',
'Tomato not Ripened',
'Walnut',
'Watermelon']

IMG_SIZE=100
def process_image(image_path):
    #read image file
    image = tf.io.read_file(image_path)
    #decode image file
    image = tf.image.decode_jpeg(image,channels=3)
    # change the image dtype to float so as to scale it between (0,1)
    image = tf.image.convert_image_dtype(image,tf.float32)
    # resize tha image
    image = tf.image.resize(image,size=[IMG_SIZE,IMG_SIZE])
    return(image)

def generate_data(img_path):
    data = tf.data.Dataset.from_tensors(tf.constant(img_path))
    data_batch = data.map(lambda i : process_image(i)).batch(32)
    return data_batch

def make_predictions(image_path,model):
    image = generate_data(image_path)
    predictions = model.predict(image)
    return(classes[predictions.argmax()])

@app.route('/', methods=['OPTIONS','POST'])
def greeting():

    def build_preflight_response():
        response = make_response("yoyoyoyoyoyoyoyoyoy")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    def build_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'OPTIONS': 
        return build_preflight_response()

    elif request.method == 'POST': 
        req = request
        url = req.get_json( )['image'].split(",")[1]
        binary_data = a2b_base64(url)
        fd = open('uploads/temp.jpg', 'wb')
        fd.write(binary_data)
        fd.close()

        model = tf.keras.models.load_model('20200613-121953_131-cat-totaldata-adam-0.978.h5')

        predicted_fruit_name = make_predictions("uploads/temp.jpg", model)

        return build_actual_response(jsonify({ 'prediction': predicted_fruit_name })),200
    
    

# @app.after_request
# def after_request(response):
#     print("log: setting cors" , file = sys.stderr)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response

if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.getenv('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
    # app.run(debug=True)