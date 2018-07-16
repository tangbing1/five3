from apps.models.base import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    sex = db.Column(db.String(3),nullable=True)
    city = db.Column(db.String(10),nullable=True)
    _password = db.Column("password", db.String(128))
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, arg):
        self._password = arg

    def __repr__(self):
        return '<User {}>'.format(self.username)