from flask import Flask, request, jsonify
# from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from PIL import Image
import os

from methodsClass import *
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import json
import random
from zipfile import ZipFile
import gdown
# load model
# path_model = "model"
# name_model = "model17_folder"
url = 'https://drive.google.com/uc?id=1ydG1A7AZj-43pcdlBvOWKtesYgrSSbbA&export=download'
output = 'build.zip'
gdown.download(url, output, quiet=False)
with ZipFile(output, 'r') as zip:
    zip.extractall()
    print('File is unzipped in temp folder')


# variables*********************************************************************
barcodeData = methodsClass.getBarCodeDataJSON('barCodeMap.json')
modelClass = methodsClass.getBarCodeDataJSON('modelClass.json')

# Load Models********************************************************************
# modelCocacolaRedcola = keras.models.load_model("modelCocacolaRedcola")
modelpte1 = keras.models.load_model("build/modelpte1", compile=False)
modelpte2 = keras.models.load_model("build/modelpte2", compile=False)
modelpte3 = keras.models.load_model("build/modelpte3", compile=False)
modelpte4 = keras.models.load_model("build/modelpte4", compile=False)
modelpte5 = keras.models.load_model("build/modelpte5", compile=False)
# modelpte6 = keras.models.load_model("modelpte6")
# modelpte7 = keras.models.load_model("modelpte7")

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    # Se recupera la imagen y se guarda con un número aleatorio*******************
    if 'image' not in request.files:
        response = 'No se proporcionó una imagen', 400
    img = request.files['image']
    numero_aleatorio = random.randint(1000, 9999)
    rutaImagen = 'service-test/'+str(numero_aleatorio)+'.jpg'
    img.save(rutaImagen)

    # Se construye la estructura de la respuesta**********************************
    inputData = {
        "barcode": int(request.form.get('barcode')),
        "class": None,
        "image": rutaImagen,
        "realibilityScore": '0'
    }

    # Clasificador****************************************************************
    model, className = methodsClass.findBarCode(
        inputData['barcode'], barcodeData)
    print(model, className)
    pathImageJpg = methodsClass.convertToJPG(inputData['image'])
    print(pathImageJpg)
    methodsClass.reduceImagen(methodsClass, pathImageJpg)

    img = image.load_img(pathImageJpg, target_size=(256, 256, 3))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Realiza la clasificación de la imagen con el modelo
    preds = None
    # if model == 'modelCocacolaRedcola':
    #    print('se ejecuta el modelo modelCocacolaRedcola')
    #    preds = modelCocacolaRedcola.predict(x)

    if model == 'modelpt1':
        print('se ejecuta el modelo 1')
        preds = modelpte1.predict(x)

    elif model == 'modelpt2':
        print('se ejecuta el modelo 2')
        preds = modelpte2.predict(x)

    elif model == 'modelpt3':
        print('se ejecuta el modelo 3')
        preds = modelpte3.predict(x)

    elif model == 'modelpt4':
        print('se ejecuta el modelo 4')
        preds = modelpte4.predict(x)

    elif model == 'modelpt5':
        print('se ejecuta el modelo 5')
        preds = modelpte5.predict(x)

    print(preds)
    posClass = methodsClass.findClassPosition(model, className, modelClass)

    # Escalar al rango [1, 10]
    # array_escalado = methodsClass.scale_to_range(preds, 1, 100)
    # print('resultadoClasificación', round(preds[0][posClass],2))
    inputData['realibilityScore'] = str(round(preds[0][posClass], 2))
    inputData['class'] = className

    return inputData


if __name__ == '__main__':
    app.run()
