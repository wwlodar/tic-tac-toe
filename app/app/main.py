from flask import Flask
from flask_migrate import Migrate

from app.config import Config
from app.extensions import csrf, db, login_manager


def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    register_extensions(app)

    with app.app_context():
        db.create_all()
        print(db.engine)
        migrate = Migrate(app, db)

    return app
