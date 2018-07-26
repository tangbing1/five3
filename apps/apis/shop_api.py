from flask import jsonify, request

from apps.apis import api_bp
from apps.apis.shop_view import shops, shop_view
from apps.models.base import db
from apps.models.user import SellerShop, Consumer
# from apps.seller_forms.seller_forms import ConsumerResForm
from apps.seller_forms.seller_forms import ConsumerResForm


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
    print(form.errors)
    return jsonify({'status':'false','message':form.errors})

@api_bp.route('/sms/',methods=['GET'])
def send_sms():
    pass