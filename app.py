from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
Bootstrap5(app)
ckeditor = CKEditor(app)

db = SQLAlchemy(app)

from routes import *
from models import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
