from flask import Blueprint, render_template, request,url_for, redirect, flash
from app import db
from models.user import User

register = Blueprint('register', __name__)

@register.route('/register', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('register.html')

    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        name = request.form['name']
        user = User.query.filter(User.user_id == user_id).first()

        if not user:
            new_user = User(user_id, user_pw, name)
            
            db.session.add(new_user)
            db.session.commit()
            
            return render_template('login.html')  

        else:
            flash('이미 존재하는 아이디입니다. 다시 입력해주세요')
            return render_template('register.html')