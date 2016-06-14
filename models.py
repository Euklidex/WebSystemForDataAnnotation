from app import db

marks = db.Table('marks',
                 db.Column('id',db.Integer, primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('block_id', db.Integer, db.ForeignKey('block.id'))
                 )


class User(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(255))
    blocks = db.relationship('Block', secondary=marks,
                           backref=db.backref('users'))

    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.blocks = []


class Block(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    words = db.relationship('Word', backref=db.backref("block"))


class Word(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30))
    block_id = db.Column(db.Integer, db.ForeignKey("block.id"))


class Answer(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category = db.Column(db.String(20))
    word = db.Column(db.String(30))
    chosen = db.Column(db.Enum("True", "False", "Error", name='answer_options'))
