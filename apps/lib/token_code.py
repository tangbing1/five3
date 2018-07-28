from functools import wraps
# wraps保护原来函数的属性
from flask import request, jsonify, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as seri, BadSignature, SignatureExpired

from apps.models.user import Consumer


def token_require(fn):
    @wraps(fn)
    def decroate(*args, **kwargs):
        token = request.cookies.get('token')
        # 这里只考虑了浏览器,如果是app的话,根据双方约定获取token
        if not token:
            return jsonify({'status': 'false', 'message': '没有token'})
        # 自动校验token
        s = seri(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            return jsonify({'status': 'false', 'message': '非法token'})
        except SignatureExpired:
            return jsonify({'status': 'false', 'message': 'token失效了'})
        uid = data.get('uid')
        user = Consumer.query.get(uid)
        if not user:
            return jsonify({'status': 'false', 'message': '没有创建该用户'})
        g.current_user = user
        # g是临时全局变量
        return fn(*args, **kwargs)
    return decroate