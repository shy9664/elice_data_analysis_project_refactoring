from flask import Blueprint, render_template, request, jsonify

from flask_jwt_extended import create_access_token, get_csrf_token, create_refresh_token, jwt_required, get_jwt_identity

from app import db
from models.user import User

from google.oauth2 import id_token
from google.auth.transport import requests

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        user = User.query.filter((User.user_id == user_id) & (User.user_pw == user_pw)).first()

        if user :
            user_info = {'user_id': user.user_id, 'name': user.name}
            access_token_cookie = create_access_token(identity=user_info)
            refresh_token_cookie = create_refresh_token(identity=user_info)
            csrf_access_token = get_csrf_token(access_token_cookie)
            res = jsonify(result='success', user_name=user.name, user_id=user.user_id, csrf_access_token=csrf_access_token)
            res.set_cookie('access_token_cookie', access_token_cookie, httponly=True)
            res.set_cookie('refresh_token_cookie', refresh_token_cookie, httponly=True)
            return res
        return jsonify({'result':'fail'})

@login.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh_token():
    user_info = get_jwt_identity()
    new_access_token = create_access_token(user_info)
    csrf_access_token = get_csrf_token(new_access_token)
    res = jsonify(result='success', csrf_access_token=csrf_access_token)
    res.set_cookie('access_token_cookie', new_access_token, httponly=True)
    return res

@login.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    res = jsonify(result='success')
    res.delete_cookie('refresh_token_cookie')
    res.delete_cookie('access_token_cookie')
    return res

@login.route('/googleLogin', methods=['POST'])
def googleLogin():
    client_id = request.form['credential[clientId]']
    token = request.form['credential[credential]']
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
    user_id = idinfo['email']
    user_pw = idinfo['sub']
    name = idinfo['name']
    user = User.query.filter(User.user_id == user_id).first()
    if not user:
        new_user = User(user_id, user_pw, name)
        db.session.add(new_user)
        db.session.commit()

    user_info = {'user_id': user_id, 'name': name}
    access_token_cookie = create_access_token(identity=user_info)
    refresh_token_cookie = create_refresh_token(identity=user_info)
    csrf_access_token = get_csrf_token(access_token_cookie)
    res = jsonify(result='success', user_name=name, user_id=user_id, csrf_access_token=csrf_access_token)
    res.set_cookie('access_token_cookie', access_token_cookie, httponly=True)
    res.set_cookie('refresh_token_cookie', refresh_token_cookie, httponly=True)
    return res