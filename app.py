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


from datetime import datetime, timedelta

def time_ago(timestamp):
    now = datetime.utcnow()
    diff = now - timestamp

    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(weeks=1):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif diff < timedelta(days=30):
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif diff < timedelta(days=365):
        months = diff.days // 30
        month_str = (timestamp.strftime("%B"))  # Full month name
        year_str = timestamp.strftime("%Y")  # Year
        return f"{month_str} {year_str}"
    else:
        year_str = timestamp.strftime("%Y")  # Year
        return f"{year_str}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
