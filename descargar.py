
import gdown
import numpy as np
import wget

# Definimos la URL del archivo a descargar

remote_url = 'https://drive.google.com/uc?id=1FagNcjLQoV7ROcl-ycadNqMtJeIZQakS&export=download/model17.h5'


url = 'https://drive.google.com/uc?id=1FagNcjLQoV7ROcl-ycadNqMtJeIZQakS&export=download'
output = 'model17.h5'
gdown.download(url, output, quiet=False)
