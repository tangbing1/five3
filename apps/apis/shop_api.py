import random

from flask import jsonify, request, current_app
from werkzeug.security import check_password_hash

from apps.apis import api_bp
from apps.apis.shop_view import shops, shop_view
from apps.lib.codes import code_view
from apps.models.base import db
from apps.models.user import SellerShop, Consumer
# from apps.seller_forms.seller_forms import ConsumerResForm
from apps.seller_forms.seller_forms import ConsumerResForm, ConsumerLoginForm
from itsdangerous import TimedJSONWebSignatureSerializer as seri

@api_bp.route('/shop_list/',methods=['GET'])
def get_shop_list():
    shop = SellerShop.query.all()
    """工作中其实是后端先做,现在是前端先做"""
    """工作中会增加数据库没有的数据,如距离,送达时间,知识点字典相加  **解包"""
    # res = [{**dict(s),**{'distance':200,'estimate_time':30}} for s in shop]
    # 在视图模型层做数据处理
    res = [shops(s) for s in shop]
    return jsonify(res)
# 获取指定店铺详细信息
# 通过?id来指定店铺
@api_bp.route('/shop/',methods=['GET'])
def get_shop():
    id = request.args.get('id',0)
    shop = SellerShop.query.filter_by(id=id).first()
    if not shop:
        return jsonify({'status':'101','message':'没有该店铺'})
    s = shop_view(shop)
    return jsonify(s)

#######################################################################################
# 用户注册
@api_bp.route('/regist/',methods=['POST'])
def regist():

    form = ConsumerResForm(request.form)
    if form.validate():
        cons = Consumer()
        cons.username = form.username.data
        cons.password = form.password.data
        cons.tel = form.tel.data
        db.session.add(cons)
        db.session.commit()
        return jsonify({'status':'true','message':'成功'})

    s = ['{}: {}'.format(k,v[0])for k,v in form.errors.items()]
    mes = '\r\n'.join(s)
    # 这里是为了让前端警告框显示错误正常点
    return jsonify({'status':'false','message':mes})

# 验证码接口
@api_bp.route('/sms/',methods=['GET'])
def send_sms():
    # 验证码应该是一个手机号一个验证码，所以这里用字典存储验证码，手机号作为key值
    tel = request.args.get('tel')
    print(tel)
    code = ''.join([str((random.randint(0, 9)))for x in range(4)])
    print('code:%s'%code)
    code_view[tel] = code
    return jsonify({"status": "true","message": "获取短信验证码为%s"%code})

# #######################################################################################
#用户登录
@api_bp.route('/login/',methods=['POST'])
def login():
    msg = "参数错误"
    login_form = ConsumerLoginForm(request.form)
    if login_form.validate():

        name = login_form.name.data
        pwd = login_form.password.data
        user = Consumer.query.filter_by(username=name).first()
        if not user:
            return jsonify({"status": "false", "message": "该用户不存在"})

        elif user and check_password_hash(user.password,pwd):

            s = seri(current_app.config['SECRET_KEY'], current_app.config['EXPIRES_TIME'])
            token = s.dumps({'uid': user.id})
            # 向下转成字节流
            res = jsonify({"status": "true", "message": "登陆成功", "user_id":str(user.id),
        "username":user.username})
            res.set_cookie('token', token.decode('utf-8'))
            # 设置cookie只能在响应中设置
            return res
        else:
            msg = "用户名或者密码错误"
    return jsonify({"status": "false","message": msg})


