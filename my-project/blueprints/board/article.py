from flask import Blueprint, render_template, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from models.article import Article

from app import db 

from datetime import datetime

from werkzeug.utils import secure_filename

import os

article = Blueprint('article', __name__, url_prefix='/article')

@article.route('/<int:article_id>', methods=['GET'])
def index(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article)

@article.route('/create', methods=['GET'])
def create_page():
    if request.method == 'GET':
        return render_template('article_form.html')

@article.route('/create', methods=['POST'])
@jwt_required()
def create():
    if request.method == 'POST':
        user_info = get_jwt_identity()
        user_id = user_info['user_id']
        name = request.form['name']
        title = request.form['title']
        content = request.form['content']
        image = request.files['image'] if request.files else None
        if image :
            image_location = 'static/uploads/' + secure_filename(image.filename)
            image.save(image_location)
        new_article = Article(user_id, name, title, content, datetime.now(), image='../'+image_location if image else None)
        db.session.add(new_article)
        db.session.commit()
        new_article = Article.query.order_by(Article.create_date.desc()).all()[0]
        return jsonify(result='success', new_article_id=new_article.id)

@article.route('/create', methods=['PATCH'])
@jwt_required()
def update():
    modified_content = request.json['modifiedContent']
    article_id = request.json['article_id']
    edited_article = Article.query.filter(Article.id == article_id).first()
    edited_article.content = modified_content
    edited_article.update_date = datetime.now()
    db.session.commit()
    return jsonify(result='success')

@article.route('/create', methods=['DELETE'])
@jwt_required()
def delete():
    article_id = request.json['article_id']
    delete_article = Article.query.filter(Article.id == article_id).first()
    db.session.delete(delete_article)
    db.session.commit()
    return jsonify(result='success')