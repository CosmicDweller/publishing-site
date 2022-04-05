from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from flask_login import LoginManager, login_manager

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = 'website/static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

uri = environ.get("DATABASE_URL")  # or other relevant config var
if str(uri).startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'kjhkjshdj fdlmfdslfj'
    app.config['SQLALCHEMY_DATABASE_URI'] = uri or f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    # from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    # app.register_blueprint(auth, url_prefix="/")

    from .models import File

    create_database(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
           

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
