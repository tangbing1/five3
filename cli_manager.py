"""维护客户端的流程"""
from flask_script import Manager
from apps import create_api_app

api_app = create_api_app()
manager = Manager(api_app)

if __name__ == '__main__':
    print(api_app.url_map)
    manager.run()