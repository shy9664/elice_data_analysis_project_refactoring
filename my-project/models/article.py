from app import db


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    create_date = db.Column(db.DateTime(), nullable=False)
    update_date = db.Column(db.DateTime(), nullable=True)


    def __init__(self, user_id, name, title, content, create_date, update_date=None, image=None):
        self.user_id = user_id
        self.name = name
        self.title = title
        self.content = content
        self.image = image
        self.create_date = create_date
        self.update_date = update_date