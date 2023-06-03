from flask import Flask
from flask_migrate import Migrate

from app.app.routes import bp
from app.extensions import csrf, db, login_manager


def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)


def create_app(config_class):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    app.register_blueprint(bp)
    register_extensions(app)

    with app.app_context():
        db.create_all()
        print(db.engine)
        migrate = Migrate(app, db, include_schemas=True)

    return app
