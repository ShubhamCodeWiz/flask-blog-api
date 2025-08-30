from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Flasgger

# configuration
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
swagger = Flasgger()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)

    # Import and register the post blueprint
    from .posts.routes import posts_bp
    app.register_blueprint(posts_bp)

    # import and register user blueprint
    from .users.routes import users_bp
    app.register_blueprint(users_bp)

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

     # Tell Flasgger about our Marshmallow schemas
    from .schemas import PostSchema, UserSchema
    app.config['SWAGGER'] = {
        'title': 'Personal Blog API',
        'uiversion': 3,
        "specs_route": "/apidocs/",
        "definitions": {
            "Post": PostSchema.Meta.fields,
            "User": UserSchema.Meta.fields
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        }
    }

    from . import models

    return app