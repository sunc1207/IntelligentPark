from flask import Blueprint
from app.api.data import yp_data
from app.api.user import yp_user
from app.api.test import yp_test
from app.api.tag import yp_tag


def create_blueprint():
    bp = Blueprint('bp_api', __name__, url_prefix='/api')
    yp_data.register(bp)
    yp_user.register(bp)
    yp_test.register(bp)
    yp_tag.register(bp)
    return bp
