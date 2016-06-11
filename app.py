from flask import Flask
from flask import render_template, request, flash, url_for, redirect, session
from forms import UserLoginForm
from models import *
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('list.html', blocks = user.blocks)

@app.route('/list/markup/<int:block_id>',  methods=['POST', 'GET'])
def markup(block_id):
    if 'name' not in session:
        return redirect(url_for('login'))
    #if request.method == 'POST':
        # do data saving
    block = Block.query.filter_by(id=block_id).first()
    return render_template('markup.html', list = block.items )

if __name__ == '__main__':
    app.run()