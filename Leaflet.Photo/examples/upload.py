import os
import sqlite3
from exif import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from tinydb import TinyDB, Query
db = TinyDB('chat_db.json')
que = Query()

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
            return render_template('cartodb.html', img_name=filename, img_url=img_url, img_lat=lat, img_lng=lng, file_url = filename)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/comment")
def comment():
    name = request.args.get("name")
    img = request.args.get('img')
    pic = request.args.get('pic')
    return render_template("comment.html",comments = db.table(name), name_f= name, img_name=img, pic=pic)


@app.route("/comment/add")
def add():
    name = request.args.get('name')
    img = request.args.get('img')
    pic = request.args.get('pic')
    print(name,"#")
    tablef = db.table(name)
    if not (tablef.search(que.user == request.args.get('user')) and (tablef.search(que.message == request.args.get('message')))):
        tablef.insert({
            'user': request.args.get('user'),
            'message': request.args.get('message')
        })
    return render_template("comment.html",comments = tablef, name_f= name, img_name=img, pic=pic)

@app.route("/comment/reset")
def reset_c():
    name = request.args.get('name')
    tablef = db.table(name)
    if tablef is not None:
        tablef.purge()
    return index()

@app.route("/reset")
def reset():
    if db is not None:
        db.purge()
    db.insert({'user': 'Pecha','message':'Welcome :)'})
    return index()


if __name__ == '__main__':
    app.debug = True
    app.run()
