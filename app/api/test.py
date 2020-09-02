from app.libs.yellowprint import YellowPrint
from app.authorization.token_auth import login_required
from flask import jsonify

yp_test = YellowPrint('yp_test', url_prefix='/test')


@yp_test.route('/test1', methods=['POST'])
def t_test():
    return 'fuck me11'


@yp_test.route('/testtest', methods=['POST'])
def t_test2():
    return 'OK'


@yp_test.route('/table')
# @login_required
def table_generation():
    return 'table'


@yp_test.route('/table1')
# @login_required
def table_generation1():
    resp = jsonify({'error': False})
    # 跨域设置
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Method'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@yp_test.route('/token')
# @login_required
def t_get_token():
    from app.authorization.token_auth import creat_token, verify_token
    s = creat_token('1')
    a = verify_token(s)
    print(s)
    print(a)
    return a


@yp_test.route('/upload')
def t_upload():
    return 'hh'


@yp_test.route('/unity', methods=['GET'])
def t_unity():
    t1 = {
        'building': 'a1'
    }
    t2 = {
        'building': 'a2'
    }
    t = {
        'data': [t1, t2]
    }
    print("It's Time Now!!")
    return t
