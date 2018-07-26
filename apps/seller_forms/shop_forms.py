from flask_login import current_user
from wtforms import Form, validators, SelectField
from wtforms import StringField, BooleanField, DecimalField

from apps.models.base import db
from apps.models.user import SellerShop, User


class ShopForm(Form):

    shop_name = StringField(label='商铺名',
                           validators=[validators.InputRequired(message='店铺名必须填写'),
                                       validators.Length(max=32, message='不能多于32个字符'),],
                            render_kw={'class': 'form-control', 'placeholder': '请输入店铺名称'},
                            )
    # 是否是品牌
    is_brand = BooleanField(label='品牌',default=False)
    # 是否准时送达
    is_ontime = BooleanField(label='准时送达',default=False)
    # 是否蜂鸟配送
    is_bird = BooleanField(label='蜂鸟配送',default=False)
    # 是否保险
    is_bao = BooleanField(label='保险',default=False)
    # 是否有发票
    is_fp = BooleanField(label='提供发票',default=False)
    # 是否准标识
    is_zun = BooleanField(label='准标识',default=False)
    # 起送价格
    start_cost = DecimalField(label='起送价格',
                              validators=[validators.InputRequired(message='起送价格必须填写'),],
                              render_kw = {'class': 'form-control', 'placeholder': '请输入起送价格'},)

    # 配送费
    send_cost = DecimalField(label='配送费',
                              validators=[validators.InputRequired(message='配送费必须填写'),],
                                          render_kw = {'class': 'form-control', 'placeholder': '请输入配送费'},)
    # 店铺公告
    notice = StringField(label='店铺公告',
                         validators=[
                                     validators.Length(max=300, message='不能多于300个字符'),
                                     ],
                        render_kw = {'class': 'form-control', 'placeholder': '请输入店铺公告'},
                         )

    # 优惠信息
    discount = StringField(label='优惠信息',
                           validators=[
                               validators.Length(max=300, message='不能多于300个字符'),
                           ],
                           render_kw={'class': 'form-control', 'placeholder': '请输入优惠信息'},)


# 店铺菜品分类
class CategoryForm(Form):
    # 分类名称
    name = StringField(label='分类名称',
                           validators=[validators.InputRequired(message='分类名必须填写'),
                                       validators.Length(max=32, message='不能多于32个字符'),
                            ])
    # 分类描述
    description = StringField(label='分类描述',
                              validators=[
                                       validators.Length(max=32, message='不能多于32个字符'),],
                              default='')
    # 是否默认
    is_default = BooleanField(label='是否默认', default=False)
    # # 归属店铺
    # shop_id = SelectField(label='归属店铺', coerce=int)
    #
    # def __init__(self, *args, **kwargs):
    #     super(CategoryForm, self).__init__(*args, **kwargs)
    #     self.shop_id.choices = []
    #     if current_user.is_authenticated:
    #         self.shop_id.choices = [(shop.id, shop.shop_name) for shop in current_user.shop]

   

# 菜品表单验证
class MenuDishesForm(Form):
    # 菜品名称
    food_name = StringField(label='菜品名称',
                           validators=[validators.InputRequired(message='菜品名必须填写'),
                                       validators.Length(max=32, message='不能多于32个字符'),
                            ])
    # 归属分类
    category_id = SelectField(label='菜品分类', coerce=int)
    # 菜品价钱
    food_price = DecimalField(label="菜品价钱", places=2,
                              validators=[validators.NumberRange(min=0, max=9999, message="价钱超出范围"),
                                          validators.InputRequired(message="请输入菜品价格"),
                                          ]
                              )
    description = StringField(label='菜品描述',
                              validators=[
                                       validators.Length(max=64, message='不能多于64个字符'),],
                              default='')
    tips = StringField(label='菜品提示信息',
                              validators=[
                                       validators.Length(max=32, message='不能多于32个字符'),],
                              default='')
    def __init__(self, sid, *args, **kwargs):
        # 通过在视图函数中实例化form表单传进的sid
        super(MenuDishesForm, self).__init__(*args, **kwargs)
        self.category_id.choices = []
        if current_user.is_authenticated:
            # 获取当前店铺
            shop = SellerShop.query.get(sid)
            self.category_id.choices = [(i.id, i.name)for i in shop.categories]
