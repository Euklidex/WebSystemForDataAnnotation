from flask import Flask
from flask import render_template, request, flash, url_for, redirect, session
from forms import UserLoginForm
from models import *
from flask_sqlalchemy import SQLAlchemy
import json
from xml import etree
from random import randint

app = Flask(__name__)
app.debug = True
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/PB138db'


db = SQLAlchemy(app)


@app.route('/',  methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = UserLoginForm(request.form)
        if form.validate():
            exists = User.query.filter_by(name=form.name.data).scalar() is not None
            if exists:
                session['name'] = form.name.data
                if session['name'] == "admin":
                    return redirect(url_for('admin'))
                return redirect(url_for('list'))
            return redirect(url_for('login'))
        else:
            flash('All fields are required.')
    form = UserLoginForm()
    return render_template('login.html',form = form)


@app.route('/list',  methods=['POST', 'GET'])
def list():
    if 'name' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(name=session['name']).first()
    if user is None:
        return redirect(url_for('login'))
    blocks = []
    for block in user.blocks:
        blocks.append(block.id)
    return render_template('list.html', blocks = blocks)


@app.route('/list/markup/<int:block_id>', methods=['POST', 'GET'])
def markup(block_id):
    if 'name' not in session:
        return redirect(url_for('login'))
     # if request.method == 'POST':
        # do data saving
    words = []
    block = Block.query.filter_by(id = block_id).first()
    for word in block.words:
        words.append(word.text)
    add_duplicates(words, 1)
    add_errors(words, 1)
    return render_template('markup.html', words=json.dumps(words), category=block.category)

@app.route('/get_data', methods=['POST', 'GET'])
def get_data():
    print("okej")
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if 'name' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            #filename = secure_filename(file.filename)
            words =  file.read().splitlines()
            category = words.pop(0)
            divide_to_blocks(category, words)
    return render_template("admin.html")


def divide_to_blocks(category, words):
    block_length = 3
    block_count = len(words) / block_length
    if len(words) % block_length != 0:
        block_count += 1
    blocks = []                                  #contains block ids
    for i in range(block_count):
        b = Block()
        b.category = category
        db.session.add(b)
        db.session.flush()
        blocks.append(b.id)
    for i in range(len(words)):
        w = Word()
        w.text = words[i]
        w.type = "Mark"
        w.block_id = blocks[i % block_count]
        db.session.add(w)
        db.session.commit()
    assign_to_user(blocks)


def assign_to_user(blocks):
    users = User.query.all()
    for i in range(2 * len(blocks)):
        db.session.execute(marks.insert(), params={'user_id': users[i % len(users)].id, 'block_id':blocks[i % len(blocks)]})
    db.session.commit()


def add_duplicates(words, part):
    for i in range(len(words)  / part):
        words.insert(randint(0, len(words)-1), words[randint(0, len(words) - 1)])


def add_errors(words, part):
    file = open('/home/user/PythonProjects/Project/Files/error.txt', 'r')
    errors = file.read().splitlines()
    for i in range(len(words) / part):
        words.insert(randint(0, len(words)-1), errors[randint(0, len(errors)-1)])

"""
def make_errors(path):
    file = open(path , 'r')
    words = file.read().splitlines()
    for i in range(len(words)):
        w = Word()
        w.text = words[i]
        w.type = "Error"
        w.block_id = blocks[i % block_count]
        db.session.add(w)
        db.session.commit()
"""

def create_xml(category):
    blocks = Block.query.filter_by(category = category).all()
    for block in blocks:
        block.words

    root = etree.Element('kategorie')
    #root.text = # category


    child = etree.Element('slova')
    child.text = 'some text'
    root.append(child)



if __name__ == '__main__':
    app.run()
