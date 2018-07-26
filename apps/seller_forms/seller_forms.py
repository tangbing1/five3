from wtforms import Form, ValidationError
from wtforms import StringField,PasswordField
from wtforms import validators
# flask_wt 里自带了csrf,如果左前后端分离,这个是用不了的
from apps.models.user import User, Consumer


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
    def validate_username(self, field):
        if User.query.filter(User.username == field.data).count() == 1:
            raise ValidationError('该用户名已经存在')

class SellerLoginForm(Form):
    username = StringField(label='用户名',
                           validators=[validators.InputRequired(message='用户名必须填写'),
                                       validators.Length(min=3, message='不能少于3个字符'),
                                       validators.Length(max=32, message='不能多于32个字符')], )
    password1 = PasswordField(label='密码',
                              validators=[validators.InputRequired(message='密码必须填写'),
                                          validators.Length(min=3, message='不能少于6个字符'),
                                          validators.Length(max=32, message='不能多于16个字符')], )

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).count() == 0:
            raise ValidationError('该用户名还没注册')


############################################################################################
# 用户注册登录表单
class ConsumerResForm(Form):
    username = StringField(label='用户名',
                           validators=[validators.InputRequired(message='用户名必须填写'),
                                       validators.Length(min=3,message='不能少于3个字符'),
                                       validators.Length(max=32,message='不能多于32个字符')],)
    password = PasswordField(label='密码',
                              validators=[validators.InputRequired(message='密码必须填写'),
                                          validators.Length(min=3, message='不能少于6个字符'),
                                          validators.Length(max=32, message='不能多于16个字符')], )
    tel = PasswordField(label='手机号',
                             validators=[validators.InputRequired(message='手机号必须填写'),
                                         validators.Length(min=3, message='不能少于11个字符'),
                                         validators.Length(max=32, message='不能多于16个字符')], )

    def validate_username(self, field):
        if Consumer.query.filter(Consumer.username == field.data).count() == 1:
            raise validators.ValidationError('该用户名已经存在')
    def validate_tel(self, field):
        if Consumer.query.filter(Consumer.tel == field.data).count() == 1:
            raise validators.ValidationError('该手机号已经存在')
