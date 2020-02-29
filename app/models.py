from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app
from .exceptions import ValidationError
from . import db, create_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    urls = db.relationship('Url', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def export_data(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }

    def import_data(self, data):
        try:
            self.name = data.get('name')
            self.email = data.get('email')
            if data.get('password') is not None:
                self.set_password(data.get('password'))
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self

    def __repr__(self):
        return '<User %r>' % self.username


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(2040))
    short = db.Column(db.String(5), unique=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def export_data(self):
        return {
            'id': self.id,
            'long': self.long,
            'short': self.short,
            'created_on': self.created_on
        }


class Click(db.Model):
    __tablename__ = 'clicks'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(2040))
    count = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
