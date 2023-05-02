from flask import Blueprint
from flask_useful import register_blueprints


bp = Blueprint('v2', __name__, url_prefix='/v2')
register_blueprints(bp, '.')
