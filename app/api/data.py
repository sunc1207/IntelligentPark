# author    : SC
# time      ：2020/9/1  18:14
# file      ：getData.PY
# project   ：apiToy
# IDE       : PyCharm

import os
from app.libs.yellowprint import YellowPrint
from app.libs.db_manager import *
from app.libs.get_temperature import get_temperature_shanghai, update_current_temperature_to_mongodb
from flask import jsonify
from flask import request

yp_data = YellowPrint('yp_data', url_prefix='/data')


@yp_data.route('/all', methods=['GET'])
def get_all_data():
    return jsonify(get_all())

@yp_data.route('/company_info', methods=['GET'])
def get_company_info():
    return jsonify(get_company())

@yp_data.route('/floor_company', methods=['GET'])
def get_floor_info():
    return jsonify(get_floor())

@yp_data.route('/co_num_info', methods=['GET'])
def get_company_data():
    co_num = request.args['co_num']
    return jsonify(get_co_num(co_num))

@yp_data.route('/temperature', methods=['GET'])
def get_temperature_data():
    res = os.fork()
    if res == 0:
        update_current_temperature_to_mongodb()
    else:
        return get_temperature_shanghai()
