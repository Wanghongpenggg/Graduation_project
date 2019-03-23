import os
from app import create_app, db
from flask_migrate import Migrate
from app.models.user import User
from app.models.user_info import UserInfo
from app.models.function_bar import FunctionBar
from app.models.mine_info import MineInfo

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


def record_init():
    test_user = User(username="test", password="123456")
    db.session.add(test_user)
    admin_user = User(username="admin", password="123456", genre=2)
    db.session.add(admin_user)
    function_list = [
        FunctionBar(function_text="标识管理", function_url="back.manage_identifier", genre=0),
        FunctionBar(function_text="矿山管理", function_url="back.manage_mine", genre=1),
        FunctionBar(function_text="企业管理", function_url="back.manage_company", genre=2),
        FunctionBar(function_text="功能列表", function_url="back.manage_function", genre=2),
    ]
    db.session.add_all(function_list)

    db.session.commit()


# 代替了在flask shell中from xxx import xxx
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, UserInfo=UserInfo, FunctionBar=FunctionBar, MineInfo=MineInfo,
                record_init=record_init)
