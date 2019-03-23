from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    #添加路由和自定义的错误页面
    from .views.auth import auth_blueprint as auth_bp
    from .views.back import back_blueprint as back_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(back_bp)
    return app
