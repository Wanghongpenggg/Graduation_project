from app import db
from datetime import datetime


class MineInfo(db.Model):
    __tablename__= 'mine_info'
    id = db.Column(db.Integer,primary_key = True)
    company_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    mine_code = db.Column(db.Text)
    mine_name = db.Column(db.Text)
    mine_loc = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    is_delete = db.Column(db.Boolean,default=0)

    def __repr__(self):
        return '<MineInfo %r>' % self.company_name
