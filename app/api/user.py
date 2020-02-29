from flask import request, g, jsonify, url_for, current_app, abort
from . import api
from .. import db, create_app
from ..models import User
from ..decorators import json, paginate
from ..auth import auth_token
from ..utils import b62_encode, b62_decode


@api.route('/user/<int:id>', methods=['GET'])
@json
@auth_token.login_required
def get_user(id):
    return User.query.get_or_404(id)


@api.route('/signup', methods=['POST'])
@json
def signup():
    user = User()
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return {'user': user.export_data()}

@api.route('/login', methods=['POST'])
@json
def login():
    user = User.query.filter_by(email=request.json.get('email')).first()
    if user is not None and user.verify_password(request.json.get('password')):
        return {'token': user.generate_auth_token(), 'user': user.export_data(), 'failed': False}
    return {'failed': True}


@api.route('/edit-user/<int:id>', methods=['POST'])
@json
@auth_token.login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if not g.user == user:
        abort(404)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return {'token': user.generate_auth_token(), 'user': user.export_data()}
