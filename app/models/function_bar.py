from app import db
from datetime import datetime
from .permission import Permission


class FunctionBar(db.Model):
    __tablename__= 'function_bar'
    id = db.Column(db.Integer,primary_key = True)
    function_text = db.Column(db.Text)
    function_url = db.Column(db.Text)
    genre = db.Column(db.Integer,default=Permission.COMPANY)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    is_delete = db.Column(db.Boolean,default=0)

    def __repr__(self):
        return '<FunctionBar %r>' % self.function_text
