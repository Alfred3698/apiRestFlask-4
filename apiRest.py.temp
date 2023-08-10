from flask import Flask, request
from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from PIL import Image
import os
from tensorflow import keras
import json

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        response = 'No se proporcionó una imagen', 400
    img = request.files['image']
    img.save('imagenFlask/test.jpg')
    
    ruta = 'imagenFlask'

    for archivo in os.listdir(ruta):
        nombre_archivo, extension = os.path.splitext(archivo)
        img = Image.open(ruta+'\\'+archivo)
        weightImg = round(os.path.getsize(ruta+'\\'+archivo)*.001)
        if weightImg >=1000:
            img.convert('RGB').save(ruta+'\\'+nombre_archivo+'.jpg', quality=50, optimize=True)
        elif weightImg >=800:
            img.convert('RGB').save(ruta+'\\'+nombre_archivo+'.jpg', quality=60, optimize=True)
        elif weightImg >=600:
            img.convert('RGB').save(ruta+'\\'+nombre_archivo+'.jpg', quality=70, optimize=True)
        elif weightImg >=500:
            img.convert('RGB').save(ruta+'\\'+nombre_archivo+'.jpg', quality=80, optimize=True)
        elif weightImg >=400:
            img.convert('RGB').save(ruta+'\\'+nombre_archivo+'.jpg', quality=90, optimize=True)
        else:
            img.convert('RGB').save(ruta+'\\'+nombre_archivo+'.jpg', quality=100, optimize=True)

        if extension == '.png':
            os.remove(ruta_carpeta+'\\'+archivo)
        elif extension == '.jpeg':
            os.remove(ruta_carpeta+'\\'+archivo)
        
    #modelo_cargado = tf.saved_model.load('modelov2.h5')
    reload = keras.models.load_model("model17_folder")

    img = image.load_img('imagenFlask/test.jpg', target_size=(256, 256, 3))

    # Convierte la imagen a un array de numpy y normaliza los valores
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Realiza la clasificación de la imagen con el modelo
    preds = reload.predict(x)
    clase = np.argmax(preds, -1)
    os.remove('imagenFlask/test.jpg')
    
    # crear un diccionario para convertir a JSON
    response = ''
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
    
    # Aquí puedes procesar la imagen como desees
    data = {
    "result": response
    }
    json_data = json.dumps(data)
    return data

if __name__ == '__main__':
    app.run()