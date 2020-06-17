from flask import Flask, request, jsonify,make_response

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import sys
import os
from PIL import Image 
from binascii import a2b_base64

import tensorflow as tf

app = Flask(__name__)

classes = [
    "Apple",
    "Banana",
    "Blueberry",
    "Cherry",
    "Dates",
    "Grapes",
    "Guava",
    'Lemon',
    "Mango",
    "Onion",
    "Orange",
    "Papaya",
    "Pineapple",
    "Pomegranate",
    "Potato",
    "Strawberry",
    "Tomato",
    "Watermelon"]

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

def generate_dataset(img_path):
    # create tensorflow dataset i.e [(X,y),(X,y)......]
    data = tf.data.Dataset.from_tensors(tf.constant(img_path))
    # create batch because our accepts data in form of batches
    data_batch = data.map(lambda i : process_image(i)).batch(32)
    return data_batch

def make_predictions(image_path,model):
    # create tf.dataset from image path
    image = generate_dataset(image_path)
    # predicting the probabilites of fruits/vegetables using our saved model
    predictions = model.predict(image)
    # returning the fruit/vegetable name having maximum probability
    return(classes[predictions.argmax()])

@app.route('/', methods=['OPTIONS','POST'])
def greeting():

    # handling the preflight request that the browser sends to check CORS
    def build_preflight_response():
        response = make_response("Preflight-Request-Response")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    # handling the actual request 
    def build_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # preflight request if of OPTIONS method
    if request.method == 'OPTIONS': 
        return build_preflight_response()

    # actual request is of POST method
    elif request.method == 'POST': 
        req = request
        # image recieved is a data URI , so splitting the base64 string from it
        url = req.get_json( )['image'].split(",")[1]
        # decoding the string to get the image
        binary_data = a2b_base64(url)
        # writing image binary data to a file in jpg format
        fd = open('uploads/temp.jpg', 'wb')
        fd.write(binary_data)
        fd.close()

        # loading the saved model
        model = tf.keras.models.load_model('20200613-080411_18-cat-totaldata-adam-0.965.h5')

        # predicting fruit using image
        predicted_fruit_name = make_predictions("uploads/temp.jpg", model)

        # returning response in JSON format
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