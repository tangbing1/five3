from apps.models.base import db
from werkzeug.security import generate_password_hash

class User(db.Model):
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