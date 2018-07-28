from wtforms import Form, ValidationError, IntegerField
from wtforms import StringField,PasswordField
from wtforms import validators
# flask_wt 里自带了csrf,如果左前后端分离,这个是用不了的
from apps.lib.codes import r
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
    TEL_REG = r'^((13[0-9])|(14[5,7])|(15[^4])|(17[0,3,5-8])|(18[0-9])|166|198|199)\d{8}$'
    username = StringField(label='用户名',
                           validators=[validators.InputRequired(message='用户名必须填写'),
                                       validators.Length(min=3,message='不能少于2个字符'),
                                       validators.Length(max=32,message='不能多于32个字符')],)
    password = PasswordField(label='密码',
                              validators=[validators.InputRequired(message='密码必须填写'),
                                          validators.Length(min=3, message='不能少于6个字符'),
                                          validators.Length(max=32, message='不能多于16个字符')], )
    tel = PasswordField(label='手机号',
                             validators=[validators.InputRequired(message='手机号必须填写'),
                                         validators.Regexp(TEL_REG, message='请填入正确的手机号')], )
    sms = StringField(label='验证码',
                      validators=[validators.InputRequired(message='验证码必须填写')],
                      )

    def validate_username(self, field):
        if Consumer.query.filter(Consumer.username == field.data).count() == 1:
            raise validators.ValidationError('该用户名已经存在')
    def validate_tel(self, field):
        if Consumer.query.filter(Consumer.tel == field.data).count() == 1:
            raise validators.ValidationError('该手机号已经存在')

    def validate_sms(self, field):
        tel = self.tel.data
        code = r.get(tel)
        code = code.decode('utf-8')
        if code != field.data:
            raise validators.ValidationError('验证码无效')


# 用户登录表单
class ConsumerLoginForm(Form):
    name = StringField(label='用户名',
                           validators=[validators.InputRequired(message='用户名必须填写'),
                                       validators.Length(min=3, message='不能少于2个字符'),
                                       validators.Length(max=32, message='不能多于32个字符')], )
    password = PasswordField(label='密码',
                             validators=[validators.InputRequired(message='密码必须填写'),
                                         validators.Length(min=3, message='不能少于6个字符'),
                                         validators.Length(max=32, message='不能多于16个字符')])
    def validate_username(self, field):
        if Consumer.query.filter(Consumer.username == field.data).count() == 0:
            raise validators.ValidationError('该用户名还没有被注册')

# 用户收货地址表单
class BuyerAddressForm(Form):
    TEL_REG = r'^((13[0-9])|(14[5,7])|(15[^4])|(17[0,3,5-8])|(18[0-9])|166|198|199)\d{8}$'
    id = IntegerField(default=0)
    name = StringField(label='名字',
                       validators=[validators.InputRequired(message='名字必须填写'),
                                  validators.Length(max=32, message='不能多于32个字符')],)
    tel = PasswordField(label='手机号',
                        validators=[validators.InputRequired(message='手机号必须填写'),
                                    validators.Regexp(TEL_REG, message='请填入正确的手机号'),])
    provence = StringField(label='省',
                           validators=[validators.InputRequired(message='省份必须填写'),
                                       validators.Length(max=32, message='不能多于32个字符')], )
    city = StringField(label='市',
                           validators=[validators.InputRequired(message='城市必须填写'),
                                       validators.Length(max=32, message='不能多于32个字符')], )
    area = StringField(label='区',
                       validators=[validators.InputRequired(message='区域必须填写'),
                                   validators.Length(max=32, message='不能多于32个字符')],)
    detail_address = StringField(label='详细地址',
                       validators=[validators.InputRequired(message='详细地址必须填写'),
                                   validators.Length(max=32, message='不能多于32个字符')], )
