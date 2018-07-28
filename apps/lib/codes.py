# # 保存验证码
# code_view = {}
#引入redis模块
import redis

#连接redis服务器
r = redis.StrictRedis(host="127.0.0.1", port=6379)
