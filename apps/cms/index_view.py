from flask import render_template, request, redirect, url_for
from apps.cms import cms_bp
# from apps.models.user import User
from apps.models.base import db
from apps.models.user import User
from apps.seller_forms.seller_forms import SellerResForm


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


@cms_bp.route('/res/', methods=['GET', 'POST'], endpoint='注册')
def i_res():
    if request.method == 'POST':
        user_form = SellerResForm(request.form)
        if user_form.validate():
            user = User()
            user.username = user_form.username.data
            user._password = user_form.password1.data
            user.sex = request.form.get('sex')
            user.city = request.form.get('city')
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('cms.登录'))

    return render_template('cms/res.html')
