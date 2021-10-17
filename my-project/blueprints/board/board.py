from flask import Blueprint, render_template, request, jsonify

from models.article import Article

from flask_jwt_extended import jwt_required

board = Blueprint('board', __name__, url_prefix='/board')

@board.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    q = Article.query.order_by(Article.create_date.desc())
    # article_list = q.all()  # 페이지네이션 아니었으면 전달해줬을 파라미터
    article_list_pagination = q.paginate(page, per_page=10)
    return render_template('board.html', article_list=article_list_pagination)

@board.route('/create', methods=['GET', 'POST'])
@jwt_required()
def create():
    if request.method == 'GET':
        return jsonify(result='success')