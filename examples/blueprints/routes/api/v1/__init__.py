from flask import Blueprint
from flask_useful import register_blueprints


bp = Blueprint('v1', __name__, url_prefix='/v1')
register_blueprints(bp, '.')
