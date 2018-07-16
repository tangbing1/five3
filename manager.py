from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from apps import create_app
from apps.models.base import db
# 创建app
app = create_app()

# 数据库的迁移
migrare = Migrate(app, db)
# 再用manager进行接管
manager = Manager(app=app)

# 注册迁移命令
manager.add_command('db', MigrateCommand)



@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    print(app.url_map)
    manager.run()
