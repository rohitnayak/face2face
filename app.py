from flask import Flask, render_template, request, send_file
from wtforms import Form, TextAreaField, validators
import pickle, sqlite3, os, numpy as np
import uuid, json
import facerecognition.recognize as REC
import base64
import io
import logging, logging.config
import sys
 
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
 
logging.config.dictConfig(LOGGING)

app=Flask(__name__)

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        if not extension: 
            extension = ".jpg"
        f_name = str(uuid.uuid4()) + extension
        f_path = os.path.join("./uploaded_images/", f_name)
        file.save(f_path)
        f_outpath = os.path.join("./rec_images/", f_name)
        logging.info("fPath is " + f_path + ", Recfile is " + f_outpath)
        REC.recognize(f_path, f_outpath)
        logging.info('Hello7')
        data = open(f_outpath, "rb").read()
        data = base64.b64encode(data)
        return send_file(io.BytesIO(data), mimetype='image/jpg')

@app.route('/')
def recognize_submit():
    return render_template('recognize_submit.html')

@app.route('/jpeg_camera/<path:path>')
def send_js(path):
    return send_file('jpeg_camera\\'+ path)

if __name__ == "__main__":
    app.run(debug=True)
