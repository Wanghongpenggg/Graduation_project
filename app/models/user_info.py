from app import db
from datetime import datetime


class UserInfo(db.Model):
    __tablename__= 'user_info'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    verify = db.Column(db.Boolean,default=0)
    verify_info = db.Column(db.Text)
    company_code = db.Column(db.Text)
    company_name = db.Column(db.Text)
    company_address = db.Column(db.Text)
    postal_code = db.Column(db.Text)
    company_phone = db.Column(db.Text)
    company_mail = db.Column(db.Text)
    area_code = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    is_delete = db.Column(db.Boolean,default=0)

    def __repr__(self):
        return '<UserInfo %r>' % self.company_name
