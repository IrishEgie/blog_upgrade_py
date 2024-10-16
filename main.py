from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import smtplib
import os


user_email = os.getenv('EMAIL')
user_pass = os.getenv('PASSWORD')
def send_email(sender_msg):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()  # Secure the connection
            connection.login(user=user_email, password=user_pass)
            
            # Create a properly formatted email message
            subject = "New Contact Form Submission"
            msg = f"Subject: {subject}\n\n{sender_msg}"
            connection.sendmail(from_addr=user_email, to_addrs=os.getenv('SENDEE'), msg=msg)
            print('Email sent successfully!')
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error. Check your email and password.")
    except smtplib.SMTPException as e:
        print(f'SMTP Error: {e}')
    except Exception as e:
        print(f'Failed to send email: {e}')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Save Post')

# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()



@app.route('/')
def home():
    blog_posts = BlogPost.query.all()
    return render_template('index.html', posts=blog_posts)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data['name']
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        print(name)
        print(email)
        print(phone)
        print(message)

        sender_msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        print(sender_msg)
        send_email(sender_msg=sender_msg)

        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog/<int:post_id>')
def blog(post_id):
    # Query the database for a specific blog post by ID
    blog_post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', blog_post=blog_post)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@app.route('/post', methods=['GET', 'POST'])  # For creating a new post
def manage_post(post_id=None):
    # If post_id is provided, we are editing an existing post
    if post_id:
        blog_post = BlogPost.query.get_or_404(post_id)
    else:
        blog_post = None

    form = PostForm(obj=blog_post)  # Prepopulate the form if editing

    if form.validate_on_submit():
        if blog_post:  # Editing an existing post
            blog_post.title = form.title.data
            blog_post.subtitle = form.subtitle.data
            blog_post.date = form.date.data
            blog_post.body = form.body.data
            blog_post.author = form.author.data
            blog_post.img_url = form.img_url.data
        else:  # Creating a new post
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=form.date.data,
                body=form.body.data,
                author=form.author.data,
                img_url=form.img_url.data
            )
            db.session.add(new_post)
        
        db.session.commit()
        return redirect(url_for('home'))  # Redirect after creation or edit

    return render_template('edit_post.html', form=form, blog_post=blog_post)


if __name__== "__main__":
    app.run(debug=True)