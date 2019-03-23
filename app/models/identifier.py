from app import db
from datetime import datetime

class Identifier(db.Model):
    __tablename__="identifier"
    id = db.Column(db.Integer,primary_key=True)
    handle = db.Column(db.Text)
    type = db.Column(db.Integer)
    the_metadata = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    is_delete = db.Column(db.Boolean,default=0)

    def __repr__(self):
        return '<Identifier %r>' % self.handle