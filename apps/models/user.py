from flask_login.mixins import UserMixin
from apps.models.base import db
from werkzeug.security import generate_password_hash,check_password_hash
# 密码加密

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    sex = db.Column(db.String(3), nullable=True)
    city = db.Column(db.String(10), nullable=True)
    status = db.Column(db.Boolean, default=True)
    _password = db.Column("password", db.String(128))
    # 读函数
    @property
    def password(self):
        return self._password

    # 写函数
    @password.setter
    def password(self, arg):
        # 密码加密
        self._password = generate_password_hash(arg)




    def __repr__(self):
        return '<User {}>'.format(self.username)

# 商家店铺信息表
class SellerShop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=True)
    # 店铺名称
    shop_name = db.Column(db.String(32), nullable=False)
    # 和商家的关联关系
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 建立一个反向关系
    seller = db.relationship("User", backref="shop")
    # 店铺logo
    shop_logo = db.Column(db.String(128), default='')
    # 店铺评分
    shop_rating = db.Column(db.Float, default=5.0)
    # 是否是品牌
    is_brand = db.Column(db.Boolean, default=False)
    # 是否准时送达
    is_ontime = db.Column(db.Boolean, default=True)
    # 是否蜂鸟配送
    is_bird = db.Column(db.Boolean, default=True)
    # 是否保险
    is_bao = db.Column(db.Boolean, default=False)
    # 是否有发票
    is_fp = db.Column(db.Boolean, default=True)
    # 是否准标识
    is_zun = db.Column(db.Boolean, default=False)
    # 起送价格
    start_cost = db.Column(db.Float, default=0.0)
    # 配送费
    send_cost = db.Column(db.Float, default=0.0)
    # 店铺公告
    notice = db.Column(db.String(210), default='')
    # 优惠信息
    discount = db.Column(db.String(210), default='')

    def keys(self):
        return "shop_name", "is_brand", "is_ontime", "is_bird", "is_bao", "is_fp", "is_zun", "start_cost", "send_cost", "notice", "discount"

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)

    def __repr__(self):
        return '<Shop {} --- {}>'.format(self.shop_name, self.seller)


# 店铺菜品分类
class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 分类名称
    name = db.Column(db.String(32))
    # 分类描述
    description = db.Column(db.String(128), default='')
    # 是否默认
    is_default = db.Column(db.Boolean, default=False)
    # 归属店铺
    shop_id = db.Column(db.Integer, db.ForeignKey('seller_shop.id'))

    shop = db.relationship('SellerShop', backref='categories')

    def keys(self):
        return "name", "description", "is_default"

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)

    def __repr__(self):
        return "<MenuCate {}>".format(self.name)

# 添加菜品
class MenuDishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 菜品名称
    food_name = db.Column(db.String(64))
    # 菜品评分
    rating = db.Column(db.Float, default=5.0)
    # 归属店铺
    shop_id = db.Column(db.Integer, db.ForeignKey('seller_shop.id'))
    # 与分类的外键关系
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'))
    cates = db.relationship('MenuCategory', backref='foods')
    # 菜品价钱
    food_price = db.Column(db.DECIMAL(6, 2), default=0.0)
    # 菜品描述
    description = db.Column(db.String(128), default='')
    # 月销售额
    month_sales = db.Column(db.Float, default=0)
    # 评分数量
    rating_count = db.Column(db.Float, default=0)
    # 菜品提示信息
    tips = db.Column(db.String(128), default='')
    # 菜品图片
    food_img = db.Column(db.String(128), default='')

    def keys(self):
        return "food_name", "category_id", "food_price", "description", "tips"

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
    def __repr__(self):
        return "Food: {}-{}".format(self.food_name, self.food_price)
##########################################################################################
# 用户的注册信息表
class Consumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(64),unique=True)
    # 手机号
    tel = db.Column(db.String(16),unique=True)
    # 密码
    _password = db.Column("password", db.String(128))
    # token
    token = db.Column(db.String(128))
    # 读函数
    @property
    def password(self):
        return self._password

    # 写函数
    @password.setter
    def password(self, arg):
        # 密码加密
        self._password = generate_password_hash(arg)

    def __repr__(self):
        return '<Consumer {}>'.format(self.username)

#收货地址
class BuyerAddressModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    user = db.relationship("Consumer", backref="addresses")
    # 省
    provence = db.Column(db.String(8))
    # 市
    city = db.Column(db.String(16))
    # 县
    area = db.Column(db.String(16))
    # 详细地址
    detail_address = db.Column(db.String(64))
    # 收货人姓名
    name = db.Column(db.String(32))
    # 收货人电话
    tel = db.Column(db.String(16))

    def keys(self):
        return "provence", "city", "area", "detail_address", "name", "tel"

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
