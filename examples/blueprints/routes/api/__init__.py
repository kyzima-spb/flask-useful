from flask import Blueprint
from flask_useful import register_blueprints


bp = Blueprint('api', __name__, url_prefix='/api')
register_blueprints(bp, '.', include_packages=True)
