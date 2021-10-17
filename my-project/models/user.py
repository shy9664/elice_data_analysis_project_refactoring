from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)  #autoincrement는 없어도 자동으로 된다고 함.
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    user_pw = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)


    def __init__(self, user_id, user_pw, name):
        self.user_id = user_id
        self.user_pw = user_pw
        self.name = name