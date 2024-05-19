from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from tasks import resize_image
import os
from os import path

app = Flask(__name__)
app.jinja_env.debug = True

# Configura esta variable al directorio donde quieras guardar las imágenes subidas

UPLOAD_FOLDER = 'F:/Descargas/Original'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')

def index():

    return render_template('index.html')

def listarArchivos():
    urlFiles = 'static/archivo/'
    return (os.listdir(urlFiles))

@app.route('/upload', methods=['POST'])

def upload_file():
    fotos = listarArchivos()
    archivo_path = 'static/archivo/'
    if 'file'not in request.files:
        return jsonify({'error':'No file part'}, 400)
    file = request.files['file']
    if file.filename=="":
        return jsonify({'error': 'No selecected file'}, 400)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
    # Aquí puedes encolar cualquier tarea de Celery necesaria, por ejemplo:
    resize_image.delay(filepath, 'F:/Descargas/my_project/static/archivo' +'/'+ filename, (800, 600))
    return render_template('download.html', list_photos = fotos, archivo_path=archivo_path)

@app.route('/upload/<string:nombreFoto>', methods=['GET','POST'])
def descargar_archivo(nombreFoto=''):
    basepath = path.dirname(__file__)
    url_File = path.join(basepath, 'static/archivo', nombreFoto)
    resp = send_file(url_File, as_attachment=True)
    return resp
if __name__ == "__main__":
    app.run(host='0.0.0.0')