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
from zipfile import ZipFile


longitud, altura = 200, 100

modelo = tf.keras.models.load_model(
    ('clasificador_marcas.h5'),
    custom_objects={'KerasLayer': hub.KerasLayer}
)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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
            return prediccion_v2(prediccion)


def categorizar(path):
    img = load_img(path)
    img = np.array(img).astype(float)/255
    img = cv2.resize(img, (224, 224))
    prediccion = modelo.predict(img.reshape(-1, 224, 224, 3))
    return np.argmax(prediccion[0], axis=-1)


def prediccion_v2(clase):
    if clase == 0:
        response = '7up'
    elif clase == 1:
        response = 'agua_bonafont'
    elif clase == 2:
        response = 'agua_ciel'
    elif clase == 3:
        response = 'agua_epura'
    elif clase == 4:
        response = 'agua_fiel'
    elif clase == 5:
        response = 'agua_penafiel'
    elif clase == 6:
        response = 'agua_skarch'
    if clase == 7:
        response = 'belight'
    elif clase == 8:
        response = 'boing'
    elif clase == 9:
        response = 'casera'
    elif clase == 10:
        response = 'cocacola'
    if clase == 11:
        response = 'delawarepunch'
    elif clase == 12:
        response = 'electrolit'
    elif clase == 13:
        response = 'fanta'
    elif clase == 14:
        response = 'fresca'
    elif clase == 15:
        response = 'fritos'
    elif clase == 16:
        response = 'fuzetea'
    elif clase == 17:
        response = 'jugo_delvallefrut'
    elif clase == 18:
        response = 'jumex'
    elif clase == 19:
        response = 'manzanitasol'
    elif clase == 20:
        response = 'mirinda'
    elif clase == 21:
        response = 'pepsi'
    elif clase == 22:
        response = 'powerade'
    elif clase == 23:
        response = 'redcola'
    elif clase == 24:
        response = 'rufles'
    elif clase == 25:
        response = 'sidralmundet'
    elif clase == 26:
        response = 'sprite'
    elif clase == 27:
        response = 'squirt'
    elif clase == 28:
        response = 'suerox'
    elif clase == 29:
        response = 'topochico'
    elif clase == 30:
        response = 'vive100'
    elif clase == 31:
        response = 'yoglala'
    elif clase == 32:
        response = 'yogyoplait'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
