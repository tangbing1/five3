from wtforms import Form
from wtforms import StringField,PasswordField
from wtforms import validators
# flask_wt 里自带了csrf,如果左前后端分离,这个是用不了的

class SellerResForm(Form):
    username = StringField(label='用户名',
                           validators=[validators.InputRequired(message='用户名必须填写'),
                                       validators.Length(min=3,message='不能少于3个字符'),
                                       validators.Length(max=32,message='不能多于32个字符')],)
    password1 = PasswordField(label='密码',
                              validators=[validators.InputRequired(message='密码必须填写'),
                                          validators.Length(min=3, message='不能少于6个字符'),
                                          validators.Length(max=32, message='不能多于16个字符')], )


    password2 = PasswordField(label='确认密码',
                                validators=[validators.InputRequired(message='密码必须填写'),
                                            validators.Length(min=3, message='不能少于6个字符'),
                                            validators.Length(max=32, message='不能多于16个字符'),
                                            validators.EqualTo('password1',message='密码必须相同'),], )
