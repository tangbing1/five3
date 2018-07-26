DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///G:\db\clmm.db'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# 如果使用session,就必须配置秘钥
SECRET_KEY = 'hard to guess string'