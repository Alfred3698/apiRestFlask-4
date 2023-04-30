
import gdown
import numpy as np
import wget
from zipfile import ZipFile

# Definimos la URL del archivo a descargar

path_model = "model"
name_model = "model17_folder"
url = 'https://drive.google.com/uc?id=1CYPcEwEFGaT3vV9HQJNmgducWRYM5uJW&export=download'
output = 'servicio_classify17.zip'
gdown.download(url, output, quiet=False)
with ZipFile(output, 'r') as zip:
    zip.extractall(path_model)
    print('File is unzipped in temp folder')
with ZipFile(path_model+"/"+name_model+".zip", 'r') as zip:
    zip.extractall(name_model)
    print('File is unzipped in temp folder :D')
