from app import db
from app import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Tagged(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column('user_id',db.Integer, db.ForeignKey('user.id'))
    id_image = db.Column('image_id',db.Integer, db.ForeignKey('nifty_image.id'))
    id_frame = db.Column('frame_id',db.Integer)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean, default=False)
    last_image_id = db.Column(db.Integer, db.ForeignKey('nifty_image.id'))
    image_section = db.Column(db.Integer)
    tags = db.relationship('NiftyImage', secondary="tagged", lazy='subquery',
        backref=db.backref('tagged', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class NiftyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250),unique=True)
