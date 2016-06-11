from app import db

marks = db.Table('marks',
                 db.Column('id', db.Integer, primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('block.id', db.Integer, db.ForeignKey('block.id'))
                 )


class User(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(255))
    blocks = db.relationship('Block', secondary=marks,
                           backref=db.backref('users', lazy='dynamic'))


class List(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    blocks = db.relationship('Block', backref=db.backref("list"))


class Block(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"))
    category = db.Column(db.String(20))
    items = db.relationship('Item', backref=db.backref("block"))


class Answer(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    chosen = db.Column(db.Enum("True", "False", "Error", name='answer_options'))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))


class Item(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(30))
    answers = db.relationship('Answer', backref=db.backref("item"))
