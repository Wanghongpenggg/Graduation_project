from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from .permission import Permission


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    genre = db.Column(db.Integer,default=Permission.COMPANY)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    is_delete = db.Column(db.Boolean,default=0)
    user_info = db.relationship('UserInfo',backref='user_info',uselist=False)
    mine_info = db.relationship('MineInfo',backref='mine_info')

    @property
    def password(self):
        raise AttributeError('已加密密码不是可读的属性')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username