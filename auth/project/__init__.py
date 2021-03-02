from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    ''' Create Flask app. '''
    
    app = Flask(__name__)
    
    app.config.from_object('project.config.FlaskConfig')

    db.init_app(app)
    with app.app_context():

        # Register blueprints.
        from project.src.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from project.src.user_cli import user_cmd_bp
        app.register_blueprint(user_cmd_bp)

        # set up DB.
        db.create_all()
        
        return app
