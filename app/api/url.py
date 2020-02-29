from flask import request, g, jsonify, url_for, current_app, redirect
from . import api
from .. import db, create_app, redis_client
from ..models import Url
from ..decorators import json, paginate
from ..auth import auth_token
from ..utils import b62_encode, b62_decode


DOMAIN_NAME = "https://lin.ks"


@api.route('/create_short_url', methods=['POST'])
@auth_token.login_required
def shorten_url():

    short_url = ''
    long_url = request.json.get('long_url')
    key = f"{long_url}:{g.user.id}"
    cached_short_url = redis_client.get(key)
    if cached_short_url:
        short_url = str(cached_short_url)
    else:
        url = Url(long=long_url, user=g.user)
        db.session.add(url)
        db.session.commit()
        short_url = b62_encode(url.id)
        url.short = short_url

        
        db.session.add(url)
        db.session.commit()
        redis_client.set(key, short_url)

    return jsonify({'short_url': f"{DOMAIN_NAME}/{short_url}"})


@api.route('/<short_url>')
def get_long_url(short_url):

    # If the long url is already cached, redirect to it.
    cached_long_url = redis_client.get(short_url)
    if cached_long_url:
        return redirect(str(cached_long_url))

    # Get it from data database, cache it and redirect.
    id = b62_decode(short_url)
    url = Url.query.get_or_404(id)
    redis_client.set(short_url, url.long)

    return redirect(url.long)

@api.route('/<short_url>', methods=['PUT'])
@auth_token.login_required
def update_short_url(short_url):

    id = b62_decode(short_url)
    print(id)
    url = Url.query.get_or_404(id)
    url.long = request.json.get('long_url')

    # Update stored data in cache
    key = f"{url.long}:{g.user.id}"
    redis_client.set(key, short_url)
    redis_client.set(short_url, url.long)

    db.session.add(url)
    db.session.commit()

    return '', 200

@api.route('/<short_url>', methods=['DELETE'])
@auth_token.login_required
def delete_short_url(short_url):

    id = b62_decode(short_url)
    print(id)
    url = Url.query.get_or_404(id)

    # Delete stored data from cache
    key = f"{url.long}:{g.user.id}"
    redis_client.delete(short_url)
    redis_client.delete(key)

    db.session.delete(url)
    db.session.commit()

    return '', 204
