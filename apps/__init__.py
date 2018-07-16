from flask import Flask
from flask_bootstrap import Bootstrap

from apps.cms import cms_bp
from apps.models.base import db

def create_app():
    app = Flask(__name__)


    # 配置数据库
    app.config.from_object('apps.private_config')
    app.config.from_object('apps.pub_config')
    # Bootstrap初始化
    Bootstrap(app)
    #数据库插件注册到app上
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(cms_bp)
    return app