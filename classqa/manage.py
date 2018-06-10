# encoding:utf-8
# 存放命令行脚本相关

from flask_script import Manager  # 存放终端写的脚本
from flask_migrate import Migrate, MigrateCommand  # 模型->表 相关操作
from app import app
from exts import db
# 需要将迁移到数据库中的模型也导入，否则不会模型迁移
from models import User, Question, Answer

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)  # migrate('db', MigrateCommand)：将所有子命令绑定到db上

if __name__ == "__main__":
    manager.run()
