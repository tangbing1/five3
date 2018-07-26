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

# 登录插件的注册
def register_bs(app):

    from apps.seller_forms.login_man import login_manager
    login_manager.init_app(app)

    login_manager.login_view = "cms.登录"
    # 定制没有登录情况下自动跳转的页面
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


    # 注册login_manager对象
    register_bs(app)


    # 注册各个蓝图
    register_bp(app)

    return app


# 注册api蓝图
def res_api(app):
    from apps.apis import api_bp
    app.register_blueprint(api_bp)
#     注册子蓝图

# 产生客户端的app
def create_api_app():
    app = Flask(__name__, static_url_path='/c', static_folder='./client_web')
    # 数据库配置
    app.config.from_object('apps.private_config')
    # 注册数据库
    register_db(app)
    # 注册蓝图
    res_api(app)
    return app
