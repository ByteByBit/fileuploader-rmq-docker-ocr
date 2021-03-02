from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Init db.
db = SQLAlchemy()

def create_app():
    ''' Create flask app. '''

    app = Flask(__name__)

    app.config.from_object('project.config.Config')

    db.init_app(app)

    with app.app_context():
        from project.src.upload import upload as upload_blueprint
        app.register_blueprint(upload_blueprint)

        db.create_all()

        return app