from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
# class Base(db.Model):
#     __abstract__ = True
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.Integer, default=1)
#
#     def set_attr(self, attrs):
#         for k, v in attrs.items():
#             if hasattr(self, k) and k != "id":
#                 setattr(self, k, v)

from .user import User


