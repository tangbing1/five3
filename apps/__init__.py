from flask import Flask
from flask_bootstrap import Bootstrap


# 注册各个蓝图对象
def register_bp(app):
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)      # 商家后台的蓝图注册

    return None


# 数据库db对象初始化
def register_db(app):
    from apps.models.base import db
    db.init_app(app)

    return None


# 产生主app对象
def create_app():
    app = Flask(__name__)

    # app配置信息
    app.config.from_object('apps.private_config')
    app.config.from_object('apps.pub_config')

    # 数据库对象注册
    register_db(app)

    # Bootstrap对象的注册
    Bootstrap(app)

    # 注册各个蓝图
    register_bp(app)

    return app
