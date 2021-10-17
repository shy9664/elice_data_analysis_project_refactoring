from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from datetime import datetime

from models.article import Article
from models.answer import Answer

from app import db

answer = Blueprint('answer', __name__, url_prefix='/article')

@answer.route('/<int:article_id>/answer', methods=['POST'])
@jwt_required()
def create(article_id):
    user_info = get_jwt_identity()
    user_id = user_info['user_id']
    name = user_info['name']
    article = Article.query.get_or_404(article_id)
    content = request.json['content']
    answer = Answer(user_id, name, content, datetime.now())
    article.answer_set.append(answer)  # article.answer_set은 Article객체와 관계된 Answer객체의 리스트로, 여기에 Answer객체를 추가하는 것.
    db.session.commit()  # 그래서 db.session.add()는 따로 하지 않는 것이고, 바로 트랜잭션을 commit하면 DB에 반영된다.  
    return jsonify(result='success')