import cv2
import os
from PIL import Image
import numpy as np
import json

class methodsClass:
    
    def findBarCode(barcode, barcodeData):
        for data in barcodeData:
            for barcodedt in data['barcodes']:
                if barcode == barcodedt:
                    return [data['model'], data['class']]

    def convertToJPG(pathImage):#C:\carpeta\archivo.png
        nombre_archivo_con_extension = os.path.basename(pathImage)
        nombre_archivo, extension = os.path.splitext(nombre_archivo_con_extension)
        if extension == '.png':
            img = Image.open(pathImage)
            img.convert('RGB').save(pathImage.replace('.png','.jpg'))
            os.remove(pathImage)
            return pathImage.replace('.png','.jpg')
        elif extension == '.jpeg':
            img = Image.open(pathImage)
            img.convert('RGB').save(pathImage.replace('.jpeg','.jpg'))
            os.remove(pathImage)
            return pathImage.replace('.jpeg','.jpg')
        return pathImage

    def reduceNumberAPercentage(numero, percentage):
        reduccion = int(numero * percentage)
        resultado = numero - reduccion
        return resultado

    def getNewSize(self, imagen_original):
        # Obtiene las dimensiones de la imagen original
        alto_original, ancho_original = imagen_original.shape[:2]
        stop = False
        while stop==False:
            if alto_original <=700 or ancho_original <=700:
                stop = True
            alto_original = self.reduceNumberAPercentage(alto_original, 0.1)
            ancho_original = self.reduceNumberAPercentage(ancho_original, 0.1)
        return [alto_original, ancho_original]

    def resizeImage(pathImage, imagen_original, ancho_original, alto_original):
        # Redimensiona la imagen
        imagen_reducida = cv2.resize(imagen_original, (ancho_original, alto_original))
        # Guardar la imagen preprocesada
        cv2.imwrite(pathImage, imagen_reducida)

        nombre_archivo, extension = os.path.splitext(pathImage)
        img = Image.open(pathImage)
        img.convert('RGB').save(nombre_archivo+'.jpg', quality=100, optimize=True)

    def reduceImagen(self, pathImage):
        # Cargar imagen en escala de color
        imagen_original = cv2.imread(pathImage)
        alto_original, ancho_original = self.getNewSize(self, imagen_original)
        self.resizeImage(pathImage, imagen_original, ancho_original, alto_original)

    def scale_to_range(arr, new_min, new_max):
        arr_min = np.min(arr)
        arr_max = np.max(arr)
        scaled_arr = (arr - arr_min) / (arr_max - arr_min) * (new_max - new_min) + new_min
        return np.round(scaled_arr, 1)


    def findClassPosition(modelName, className, modelClass):
        for model in modelClass:
            if model['model'] == modelName:
                return model['class'][className]

    def getBarCodeDataJSON(filePath):    
        # Cargar el JSON array desde el archivo en una lista de Python
        with open(filePath) as archivo:
            return json.load(archivo)
        
    
    def rename_image(old_filename, new_filename):
        try:
            os.rename(old_filename, new_filename)
            print(f"Archivo {old_filename} renombrado a {new_filename} con éxito.")
        except FileNotFoundError:
            print(f"El archivo {old_filename} no existe.")
        except FileExistsError:
            print(f"El archivo {new_filename} ya existe.")