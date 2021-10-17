from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key_for_flash'

    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    from models.user import User
    from models.article import Article
    from models.answer import Answer

    from blueprints.main import main
    from blueprints.login import login
    from blueprints.register import register
    from blueprints.board.board import board
    from blueprints.board.article import article
    from blueprints.board.answer import answer
    
    app.register_blueprint(main)
    app.register_blueprint(login)
    app.register_blueprint(register)
    app.register_blueprint(board)
    app.register_blueprint(article)
    app.register_blueprint(answer)

    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.expires_access
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.expires_refresh
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    JWTManager(app)

    return app


if __name__ == '__main__' :
    create_app().run(debug=True)