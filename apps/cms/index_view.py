from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, current_user,login_required
from apps.cms import cms_bp
# from apps.models.user import User
from apps.models.base import db
from apps.models.user import User
from apps.seller_forms.seller_forms import SellerResForm, SellerLoginForm


@cms_bp.route('/index/',endpoint='主页')
def index():
    # print(session['username'])
    if current_user.is_authenticated:
        return render_template('cms/index.html')
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
        return render_template('cms/res.html',user_form=user_form)
# 注销功能
@cms_bp.route('/logout/',endpoint='注销')
def i_logout():
    # session.permanent = False
    # session['username'] = ''
    # 或者字典删除方式 session.clear()
    logout_user()
    return redirect(url_for('cms.主页'))
    # return redirect('/index/')


@cms_bp.route('/shop/',endpoint='商家资料')
@login_required
def seller_shop():
    return '商家资料'