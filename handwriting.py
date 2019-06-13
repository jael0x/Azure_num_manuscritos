# Biblioteca para realizar solicitudes http
import requests

# Módulo para manejar tareas relacionadas al tiempo y la fecha
import time

# Para que se agreguen los gráfico a la interfaz de Jupyter notebook, en caso de usarla
#%matplotlib inline

# Es una biblioteca para generar gráficos, histogramas, diagrama de dispersión
# Es una colección de funciones para que matplotlib funcione como Matlab
import matplotlib.pyplot as plt
# Es una colección de funciones para graficar polígonos
from matplotlib.patches import Polygon

# Es un módulo para representar o cargar imágenes
from PIL import Image

# Este módulo implementa una clase similar a un archivo
from io import BytesIO

# Key y url para acceder a las funciones de la api para reconocimiento de imágenes de Azure
subscription_key = "9b30e0e3417c4db780d7c91309124f95"
assert subscription_key
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
text_recognition_url = vision_base_url + "read/core/asyncBatchAnalyze"

# Url de la imagen que se desea analizar
image_url = "https://firebasestorage.googleapis.com/v0/b/bring2me-e3467.appspot.com/o/NumerosMejorados.jpeg?alt=media&token=1f2f87dd-f8f4-46b0-baa9-a9c44cde55a7"

# Extraer textos manuscritos require de dos llamadas a la API:
# La primera para enviar la imagen a procesar, y la segunda para obtener el texto encontrado en la imagen

# Envío de la imagen a reconocer hacia la api de Azure
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
data    = {'url': image_url}
response = requests.post(
    text_recognition_url, headers=headers, json=data)
response.raise_for_status()

# Contiene la URI usada para obtener el texto reconocido
operation_url = response.headers["Operation-Location"]

# El texto reconocido no está disponible de inmediato, por lo tanto, se realiza una consulta para esperar a que se complete
analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()
    print(analysis)
    time.sleep(1)
    if ("recognitionResults" in analysis):
        poll= False 
    if ("status" in analysis and analysis['status'] == 'Failed'):
        poll= False

polygons=[]
if ("recognitionResults" in analysis):
    #  Extraer el texto reconocido, con cuadros delimitadores
    polygons = [(line["boundingBox"], line["text"])
        for line in analysis["recognitionResults"][0]["lines"]]

# Obtiene las imagenes y las superpone con el texto extraído
plt.figure(figsize=(15, 15))
image = Image.open(BytesIO(requests.get(image_url).content))
ax = plt.imshow(image)
for polygon in polygons:
    vertices = [(polygon[0][i], polygon[0][i+1])
        for i in range(0, len(polygon[0]), 2)]
    text     = polygon[1]
    patch    = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
    ax.axes.add_patch(patch)
    plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
    print(text)