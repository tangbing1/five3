from flask import render_template, request, redirect, url_for, session, flash,abort
from sqlalchemy import func
from werkzeug.datastructures import MultiDict
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, current_user,login_required
from apps.cms import cms_bp
# from apps.models.user import User
from apps.models.base import db
from apps.models.user import User, SellerShop, MenuCategory, MenuDishes
from apps.seller_forms.seller_forms import SellerResForm, SellerLoginForm
from apps.seller_forms.shop_forms import ShopForm, CategoryForm, MenuDishesForm

# ########################################################################
# 通用函数块
##########################################################################
# 检查shop_id的合法性
@login_required
def check_shop_id(sid):
    # 必须查找当前商家的店铺,所以必须满足两个条件,万一另一个商家也有这个id会乱套
    shop = SellerShop.query.filter_by(id=sid, seller_id=current_user.id).first()
    if not shop:
        abort(redirect(url_for('cms.主页')))
    return shop
###############################################################################
@cms_bp.route('/index/',endpoint='主页')
def index():
    # print(session['username'])
    if current_user.is_authenticated:

        shop_info = db.session.query(SellerShop.shop_name, SellerShop.start_cost, SellerShop.send_cost, SellerShop.shop_rating, SellerShop.id).join(User).filter(User.username == current_user.username).all()
        print(shop_info)
        # print(current_user.shop)

        return render_template('cms/index.html', shop_info=shop_info)
    return render_template('cms/index.html')



# 登录功能
@cms_bp.route('/login/',methods=['GET','POST'],endpoint='登录')
def i_login():
    if request.method == 'POST':
        user_form = SellerLoginForm(request.form)
        if user_form.validate():
            user = User.query.filter(User.username == user_form.username.data).first()
            if user == None:
                flash('该用户名不存在')
                return redirect(url_for('cms.登录'))
            elif user != None and check_password_hash(user.password, user_form.password1.data):
                # password和_password要区别,数据库里没有_password
                # session.permanent = True
                # session['username'] = request.form['username']
                # flash('You were logged in')
                """利用session来记录登录状态"""
                """利用login插件来做登录"""
                login_user(user)
                # 判断是否传递了next的参数
                next_page = request.args.get('next')
                print(next_page)
                if not next_page or not next_page.startswith('/'):
                    # 判断next_page.startswith('/')为了防止黑客攻击比如
                    # http://127.0.0.1:5000/login/?next=www.baidu.com
                    next_page = url_for('cms.主页')
                return redirect(next_page)

            else:
                flash('密码错误')
                user_form.password1.errors = ['用户名或者密码错误']
                return render_template('cms/login.html', user_form=user_form)
        else:
            return render_template('cms/login.html', user_form=user_form)
    else:
        user_form = SellerLoginForm(request.form)
        return render_template('cms/login.html', user_form=user_form)


# 注册功能
@cms_bp.route('/res/', methods=['GET', 'POST'], endpoint='注册')
def i_res():
    if request.method == 'POST':
        # 利用用户输入的数据,实例化表单验证器,使用用户的post提交的数据
        user_form = SellerResForm(request.form)
        # 利用验证器模块的校验方式,检验数据
        if user_form.validate():
            user = User()
            user.username = user_form.username.data
            user.password = generate_password_hash(user_form.password1.data)
            # 密码加密
            user.sex = request.form.get('sex')
            user.city = request.form.get('city')
            # 性别和城市可以不用填,所以不用在form表单里验证,直接获取,
            db.session.add(user)
            db.session.commit()
            """利用session做登录"""
            # session.permanent = True
            # session['username'] = request.form['username']
            # flash('You were logged in')
            # 利用session来记录登录状态
            """利用flask_login做登录"""
            login_user(user)

            return redirect(url_for('cms.主页'))
        # 错误都保存在user_form的errors里,可以debug模式查看
        return render_template('cms/res.html', user_form=user_form)
    else:
        user_form = SellerResForm(request.form)
        return render_template('cms/res.html', user_form=user_form)
# 注销功能
@cms_bp.route('/logout/',endpoint='注销',)
def i_logout():
    # session.permanent = False
    # session['username'] = ''
    # 或者字典删除方式 session.clear()
    logout_user()
    return redirect(url_for('cms.主页'))
    # return redirect('/index/')

# @login_required判断用户是否登录

@cms_bp.route('/add_shop/',endpoint='添加店铺',methods=['GET', 'POST'])
@login_required
def add_shop():
    if request.method == 'POST':
        form = ShopForm(request.form)
        if form.validate():
            shop = SellerShop()
            shop.shop_name = form.shop_name.data
            shop.seller_id = current_user.id
            shop.is_brand = form.is_brand.data
            shop.is_ontime = form.is_ontime.data
            shop.is_bird = form.is_bird.data
            shop.is_bao = form.is_bao.data
            shop.is_fp = form.is_fp.data
            shop.is_zun = form.is_zun.data
            shop.start_cost = form.start_cost.data
            shop.send_cost = form.send_cost.data
            shop.notice = form.notice.data
            shop.discount = form.discount.data
            db.session.add(shop)
            db.session.commit()
            return redirect(url_for('cms.主页'))

        return render_template('cms/add_shop.html', form=form)
    else:
        form = ShopForm(request.form)
        return render_template('cms/add_shop.html', form=form)

@cms_bp.route('/add_cate/<int:sid>/',endpoint='添加分类',methods=['GET', 'POST'])
@login_required
def add_cate(sid):
    # 检查shop合法性
    shop = check_shop_id(sid)
    cate_form = CategoryForm(request.form)
    if request.method == 'POST' and cate_form.validate():
        cate = MenuCategory()
        cate.name = cate_form.name.data
        cate.description = cate_form.description.data
        cate.is_default = cate_form.is_default.data
        cate.shop_id = shop.id
        db.session.add(cate)
        db.session.commit()

        return redirect(url_for('cms.主页'))
    return render_template('cms/add_cate.html', form=cate_form)
@cms_bp.route('/show_cate/<int:sid>/',endpoint='显示分类')
@login_required
def show_cate(sid):
    #检查sid合法性
    shop = check_shop_id(sid)
    # s = SellerShop.query.filter(SellerShop.id == sid).first()

    cates = shop.categories

    # 菜品数量
    result = [{'name': cate.name, 'count': len(cate.foods),'id': cate.id,'total':'%.2f'%(sum([x.food_price for x in cate.foods])/(len(cate.foods) if len(cate.foods)>0 else 1))}for cate in cates]
    # print(result)


    return render_template('cms/show_cate.html', cate=result, shop=shop)

@cms_bp.route('/add_food/<int:sid>/',endpoint='添加菜品',methods=['GET', 'POST'])
@login_required
def add_food(sid):
    # 检查sid合法性
    shop = check_shop_id(sid)
    food_form = MenuDishesForm(sid, request.form)
    # 如果form表单的下拉框没有在form中定义,就在视图函数中用以下方法
    # shop = SellerShop.query.filter(SellerShop.id == int(sid)).first()
    # food_form.category_id.choices = [(i.id, i.name)for i in shop.categories]
    if request.method == 'POST' and food_form.validate():
        food = MenuDishes()
        food.food_name = food_form.food_name.data
        food.category_id = food_form.category_id.data
        food.food_price = food_form.food_price.data
        food.description = food_form.description.data
        food.tips = food_form.tips.data
        food.shop_id = shop.id
        db.session.add(food)
        db.session.commit()
        return redirect(url_for('cms.添加菜品', sid=shop.id))
    return render_template('cms/add_food.html', form=food_form)

@cms_bp.route('/show_food/<int:sid>/',endpoint='显示菜品')
@login_required
def show_food(sid):
    # 检查sid合法性
    shop = check_shop_id(sid)
    # s = SellerShop.query.filter(SellerShop.id == sid).first()
    cate = shop.categories
    print(cate)
    # result = [for i in cate.foods]

    return render_template('cms/show_food.html', shop=shop, cate=cate)

#############################################################################
# 更新功能
##############################################################################
@cms_bp.route('/update_shop/<int:sid>/',endpoint='更新店铺',methods=['GET', 'POST'])
@login_required
def update_shop(sid):
    shop = check_shop_id(sid)

    if request.method == 'GET':
        form = ShopForm(data=dict(shop))
        # print(form)
        # print(form.is_brand.data)
        # data这里是Form表单内源码里定义的,可以接收一个字典
        return render_template('cms/update_shop.html', form=form)

    elif request.method == 'POST':
        form = ShopForm(request.form)
        if form.validate():
            shop.shop_name = form.shop_name.data
            shop.is_brand = form.is_brand.data
            shop.is_ontime = form.is_ontime.data
            shop.is_bird = form.is_bird.data
            shop.is_bao = form.is_bao.data
            shop.is_fp = form.is_fp.data
            shop.is_zun = form.is_zun.data
            shop.start_cost = form.start_cost.data
            shop.send_cost = form.send_cost.data
            shop.notice = form.notice.data
            shop.discount = form.discount.data
            db.session.add(shop)
            db.session.commit()
            return redirect(url_for('cms.主页'))

        return render_template('cms/update_shop.html', form=form)

@cms_bp.route('/update_cate/<int:sid>/<int:cid>/',endpoint='更新分类',methods=['GET', 'POST'])
@login_required
def update_cate(sid, cid):
    shop = check_shop_id(sid)
    cate = MenuCategory.query.filter(MenuCategory.id==cid,MenuCategory.shop_id==shop.id).first()


    if request.method == 'GET':
        form = CategoryForm(data=dict(cate))
        # 把对象字典化

        return render_template('cms/update_cate.html', form=form)

    elif request.method == 'POST':
        form = CategoryForm(request.form)
        if form.validate():

            cate.name = form.name.data
            cate.description = form.description.data
            cate.is_default = form.is_default.data
            cate.shop_id = shop.id
            db.session.add(cate)
            db.session.commit()

            return redirect(url_for('cms.主页'))
        return render_template('cms/update_cate.html', form=form)

@cms_bp.route('/update_food/<int:sid>/<int:cid>/<int:fid>/',endpoint='更新菜品',methods=['GET', 'POST'])
@login_required
def update_food(sid, cid, fid):
    shop = check_shop_id(sid)
    cate = MenuCategory.query.filter(MenuCategory.id == cid, MenuCategory.shop_id == shop.id).first()
    food = MenuDishes.query.filter(MenuDishes.id==fid,MenuDishes.category_id==cate.id).first()
    if request.method == 'GET':
        form = MenuDishesForm(sid, data=dict(food))

        return render_template('cms/update_food.html', form=form)

    elif request.method == 'POST':
        form = MenuDishesForm(sid, request.form)
        if form.validate():
            # 检验form表单传来的值的合法性

            food.food_name = form.food_name.data
            food.category_id = form.category_id.data
            food.food_price = form.food_price.data
            food.description = form.description.data
            food.tips = form.tips.data

            db.session.add(food)
            db.session.commit()
            return redirect(url_for('cms.显示菜品', sid=shop.id))


        return render_template('cms/update_food.html', form=form)