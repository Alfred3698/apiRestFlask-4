from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for
import tensorflow_hub as hub
from tensorflow.keras.utils import load_img, img_to_array
import tensorflow as tf
import os
import numpy as np
import gdown
from keras.models import load_model
import cv2

url = 'https://drive.google.com/uc?id=1FagNcjLQoV7ROcl-ycadNqMtJeIZQakS&export=download'
output = 'model17.h5'
gdown.download(url, output, quiet=False)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
modelo = tf.keras.models.load_model(
    ('model17.h5'),
    custom_objects={'KerasLayer': hub.KerasLayer}
)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


@app.route('/')
def hello_world():
    return 'Hola mundo'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                print("iniciando creación de folder")
                os.stat(UPLOAD_FOLDER)
            except:
                os.mkdir(UPLOAD_FOLDER)
            print("iniciando guardado de archivo")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("iniciando prediccion")
            prediccion = categorizar(UPLOAD_FOLDER+'/'+filename)
            os.remove(UPLOAD_FOLDER+'/'+filename)
            return prediccion_(prediccion)


def categorizar(path):
    img = load_img(path)
    img = np.array(img).astype(float)/255
    img = cv2.resize(img, (224, 224))
    prediccion = modelo.predict(img.reshape(-1, 224, 224, 3))
    print("prediccion", prediccion[0])
    return np.argmax(prediccion[0], axis=-1)


def prediccion_(clase):
    if clase == 0:
        response = '7up'
    elif clase == 1:
        response = 'Ciel'
    elif clase == 2:
        response = 'epura'
    elif clase == 3:
        response = 'fiel'
    elif clase == 4:
        response = 'peñafiel'
    elif clase == 5:
        response = 'skarch'
    if clase == 6:
        response = 'boing'
    elif clase == 7:
        response = 'casera'
    elif clase == 8:
        response = 'cocacola'
    elif clase == 9:
        response = 'delaware'
    if clase == 10:
        response = 'delvalle'
    elif clase == 11:
        response = 'jumex'
    elif clase == 12:
        response = 'redcola'
    elif clase == 13:
        response = 'sidral'
    elif clase == 14:
        response = 'suerox'
    elif clase == 15:
        response = 'topochico'
    if clase == 16:
        response = 'Vive100'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
