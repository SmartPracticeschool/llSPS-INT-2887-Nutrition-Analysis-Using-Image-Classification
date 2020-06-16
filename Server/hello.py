from flask import Flask, request, jsonify,make_response

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import sys
import os
from PIL import Image 
from binascii import a2b_base64

import tensorflow as tf

app = Flask(__name__)

# all 131 classes of fruits/vegetables
classes = ['Apple Braebun', 'Apple Crimson Snow', 'Apple', 'Apple', 'Apple', 'Apple Granny Smith', 'Apple Pink Lady', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apricot', 'Avocado', 'Avocado ripe', 'Banana', 'Banana Lady Finger', 'Banana Red', 'Beetroot', 'Blueberry', 'Cactus fruit', 'Cantaloupe', 'Cantaloupe', 'Carambula', 'Cauliflower', 'Cherry', 'Cherry', 'Cherry Rainier', 'Cherry Wax Black', 'Cherry Wax Red', 'Cherry Wax Yellow', 'Chestnut', 'Clementine', 'Cocos', 'Corn', 'Corn Husk', 'Cucumber Ripe', 'Cucumber Ripe', 'Dates', 'Eggplant', 'Fig', 'Ginger Root', 'Granadilla', 'Grape Blue', 'Grape Pink', 'Grape White', 'Grape White', 'Grape White', 'Grape White', 'Grapefruit Pink', 'Grapefruit White', 'Guava', 'Hazelnut', 'Huckleberry', 'Kaki', 'Kiwi', 'Kohlrabi', 'Kumquats', 'Lemon', 'Lemon Meyer', 'Limes', 'Lychee', 'Mandarine', 'Mango', 'Mango', 'Mangostan', 'Maracuja', 'Melon Piel de Sapo', 'Mulberry', 'Nectarine', 'Nectarine', 'Nut', 'Nut', 'Onion', 'Onion', 'Onion', 'Orange', 'Papaya', 'Passion Fruit', 'Peach', 'Peach', 'Peach', 'Pear', 'Pear', 'Pear Abate', 'Pear Forelle', 'Pear Kaiser', 'Pear Monster', 'Pear Red', 'Pear Stone', 'Pear Williams', 'Pepino', 'Pepper Green', 'Pepper Orange', 'Pepper Red', 'Pepper Yellow', 'Physalis', 'Physalis with Husk', 'Pineapple', 'Pineapple Mini', 'Pitahaya Red', 'Plum', 'Plum', 'Plum', 'Pomegranate', 'Pomelo Sweetie', 'Potato', 'Potato', 'Potato', 'Potato', 'Quince', 'Rambutan', 'Raspberry', 'Redcurrant', 'Salak', 'Strawberry', 'Strawberry Wedge', 'Tamarillo', 'Tangelo', 'Tomato', 'Tomato', 'Tomato', 'Tomato', 'Tomato','Cherry Red', 'Tomato', 'Tomato', 'Tomato', 'Tomato', 'Walnut', 'Watermelon']

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
        model = tf.keras.models.load_model('20200613-121953_131-cat-totaldata-adam-0.978.h5')

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