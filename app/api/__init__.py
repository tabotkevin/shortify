from flask import Blueprint
from ..auth import auth_token
from ..decorators import etag
from .. import limiter

api = Blueprint('api', __name__)


@api.before_request
@limiter.rate_limit(limit=20, period=15)
def before_request():
    """All routes in this blueprint rate limited."""
    pass


@api.after_request
def after_request(rv):
    """Generate an ETag header for all routes in this blueprint."""
    return rv

from . import user, url