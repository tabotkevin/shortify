from flask import request, g, jsonify, url_for, current_app, redirect
from . import api
from .. import db
from ..models import Url
from ..auth import auth_token
from ..utils import b62_encode, b62_decode
from ..clients import RedisClient


DOMAIN_NAME = "https://lin.ks"
client = RedisClient()

@api.route('/create_short_url', methods=['POST'])
@auth_token.login_required
def shorten_url():

    short_url = ''
    long_url = request.json.get('long_url')
    print('checking cache')
    cached_short_url = client.get_short_url(long_url, g.user.id)
    if cached_short_url:
        print('found cache')
        short_url = cached_short_url
    else:
        print('Using the database no cache found')
        url = Url(long=long_url, user=g.user)
        db.session.add(url)
        db.session.commit()
        short_url = b62_encode(url.id)
        print('short_url is :', short_url)
        url.short = short_url

        
        db.session.add(url)
        db.session.commit()
        client.set_short_url(long_url, g.user.id, short_url)

    return jsonify({'short_url': f"{DOMAIN_NAME}/{short_url}"})


@api.route('/<short_url>')
def get_long_url(short_url):

    # If the long url is already cached, redirect to it.
    cached_long_url = client.get_long_url(short_url)
    if cached_long_url:
        return redirect(cached_long_url)

    # Get it from data database, cache it and redirect.
    id = b62_decode(short_url)
    url = Url.query.get_or_404(id)
    client.set_long_url(short_url, url.long)

    return redirect(url.long)

@api.route('/<short_url>', methods=['PUT'])
@auth_token.login_required
def update_short_url(short_url):

    id = b62_decode(short_url)
    url = Url.query.get_or_404(id)
    url.long = request.json.get('long_url')

    # Update data in cached urls
    client.set_short_url(url.long, g.user.id, short_url)
    client.set_long_url(short_url, url.long)

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
    client.delete_short_url(url.long, g.user.id)
    client.delete_long_url(short_url)

    db.session.delete(url)
    db.session.commit()

    return '', 204
