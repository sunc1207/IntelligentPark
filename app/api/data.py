# author    : Charles
# time      ：2020/7/8  18:14 
# file      ：getData.PY
# project   ：apiToy
# IDE       : PyCharm

import os
from app.libs.yellowprint import YellowPrint
from app.libs.db import get_data_from_db
from app.libs.get_temperature import get_temperature_shanghai, update_current_temperature_to_mongodb
from flask import jsonify

yp_data = YellowPrint('yp_data', url_prefix='/data')


@yp_data.route('/all', methods=['GET'])
def get_data():
    return jsonify(get_data_from_db())


@yp_data.route('/temperature', methods=['GET'])
def get_temperature_data():
    res = os.fork()
    if res == 0:
        update_current_temperature_to_mongodb()
    else:
        return get_temperature_shanghai()