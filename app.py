from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
Bootstrap5(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

from routes import *
from models import *


def create_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_db()  # Only run this when starting the app locally
    app.run()
