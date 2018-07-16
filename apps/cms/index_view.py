from flask import render_template, request, redirect, url_for, session, flash
from apps.cms import cms_bp
# from apps.models.user import User
from apps.models.base import db
from apps.models.user import User
from apps.seller_forms.seller_forms import SellerResForm, SellerLoginForm


@cms_bp.route('/index/',endpoint='主页')
def index():
    # print(session['username'])
    if session:

        return render_template('cms/index.html',name=session)
    return render_template('cms/index.html')

# 登录功能
@cms_bp.route('/login/',methods=['GET','POST'],endpoint='登录')
def i_login():
    if request.method == 'POST':
        user_form = SellerLoginForm(request.form)
        if user_form.validate():
           num = User.query.filter(User.username == user_form.username.data,
                              User._password == user_form.password1.data).count()
           if num:
               session.permanent = True
               session['username'] = request.form['username']
               flash('You were logged in')
               # 利用session来记录登录状态
               return redirect(url_for('cms.主页'))
        return render_template('cms/login.html', user_form=user_form)
    return render_template('cms/login.html')



# 注册功能
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
            # 性别和城市可以不用填,所以不用再form表单里验证,直接获取,
            db.session.add(user)
            db.session.commit()


            return redirect(url_for('cms.登录'))

        return render_template('cms/res.html', user_form=user_form)
    else:

        return render_template('cms/res.html')

@cms_bp.route('/logout/',endpoint='注销')
def i_logout():
    session.permanent = False
    session['username'] = ''
    return redirect(url_for('cms.主页'))