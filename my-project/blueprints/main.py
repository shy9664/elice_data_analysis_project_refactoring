from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/', methods=['POST'])
@jwt_required()
def analyze():
    return jsonify(result='success')
