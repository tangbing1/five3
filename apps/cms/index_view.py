from flask import render_template, request, redirect, url_for
from apps.cms import cms_bp
# from apps.models.user import User
from apps.models.base import db
from apps.models.user import User


@cms_bp.route('/index/',endpoint='主页')
def index():
    return render_template('cms/index.html')

@cms_bp.route('/login/',methods=['GET','POST'],endpoint='登录')
def i_login():
    name = request.form.get('username')
    password = request.form.get('password')
    num = User.query.filter(User.username == name, User._password == password).count()
    if num:
        return redirect(url_for('cms.主页'))
    return render_template('cms/login.html')


@cms_bp.route('/res/',methods=['GET','POST'],endpoint='注册')
def i_res():
    name = request.form.get('username')
    sex = request.form.get('sex')
    city = request.form.get('city')
    password = request.form.get('password')
    password1 = request.form.get('password1')
    if password != password1:
        return render_template('cms/res.html')
    else:
        u = User()
        u.username = name
        u.sex = sex
        u.city = city
        u._password = password
        db.session.add(u)
        db.session.commit()
        #为什么一提交就报错
        return render_template('cms/res.html')