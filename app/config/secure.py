# 密钥等敏感信息配置
# 开发/生产环境不同的配置
import os

SECRET_KEY = os.urandom(24)

# DATABASE
DATABASE = 'TODO'
DRIVER = 'TODO'
HOST = 'TODO'
PORT = 'TODO'
DATABASE = 'TODO'
USERNAME = 'TODO'
PASSWORD = 'TODO'

SQLALCHEMY_DATABASE_URI = 'TODO+TODO://TODO:TODO@TODO:TODO/TODO'
# SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
#     DATABASE, DRIVER, USERNAME, PASSWORD, HOST, PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True