from app import db


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    article = db.relationship('Article', backref=db.backref('answer_set'))
    user_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    update_date = db.Column(db.DateTime(), nullable=True)


    def __init__(self, user_id, name, content, create_date, update_date=None):
        self.user_id = user_id
        self.name = name
        self.content = content
        self.create_date = create_date
        self.update_date = update_date