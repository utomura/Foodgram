import os
import sqlite3
from exif import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'JPG'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = 'static/' + filename
            lat, lng = get_gps(img_url)
            return render_template('cartodb.html', img_name=filename, img_url=img_url, img_lat=lat, img_lng=lng)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
