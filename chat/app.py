from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from tinydb import TinyDB, Query
db = TinyDB('chat_db.json')
que = Query()

#@app.route("/")
#def index():
#    return render/template()


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/comment")
def comment():
    name = request.args.get("name")
    img = request.args.get('img')
    return render_template("comment.html",comments = db.table(name), name_f= name, img_name=img)


@app.route("/comment/add")
def add():
    name = request.args.get('name')
    img = request.args.get('img')
    print(name,"#")
    tablef = db.table(name)
    if not (tablef.search(que.user == request.args.get('user')) and (tablef.search(que.message == request.args.get('message')))):
        tablef.insert({
            'user': request.args.get('user'),
            'message': request.args.get('message')
        })
    return render_template("comment.html",comments = tablef, name_f= name, img_name=img)

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

if __name__ == "__main__":
    app.run(debug = True, port=5000, host="0.0.0.0")

