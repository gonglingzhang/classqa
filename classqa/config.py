# encoding:utf-8
# 存放一些配置参数


DEBUG = True

SECRET_KEY = b'\x05O7\xe8#\xcd\xa7\xfcm\xa7\xf4m\x93\xd1\xb8\xa1\xdc\x98\x10Uz\x8en\xff'

USERNAME = "root"
PASSWORD = "root"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "classqa"
SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
