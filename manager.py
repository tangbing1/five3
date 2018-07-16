from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from apps import create_app
from apps.models.base import db
# 创建app
app = create_app()
manager = Manager(app=app)


# 数据库的迁移
migrare = Migrate(app,db)
manager.add_command('db',MigrateCommand)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    print(app.url_map)
    manager.run()
