from flask_login import LoginManager

from apps.models.user import User

login_manager = LoginManager()


# 回调函数
@login_manager.user_loader
def load_user(userid):
    # 参考文档 http://www.pythondoc.com/flask-login/#id1
    # 文档写的是User.get(userid)意思是通过user模型获取id,这里不能完全按照他的写,要理解意思
    return User.query.get(int(userid))
    # 因为数据表的id是数字类型,而传进来的id是字符串,所以要强转
