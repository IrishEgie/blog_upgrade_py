from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager, time_ago
from models import BlogPost, Comment, User
from forms import CommentForm, LoginForm, PostForm, RegistrationForm
from email_utils import send_email
from sqlalchemy.exc import IntegrityError
#--------------------------------------- Home #--------------------------------------- #
@app.route('/')
def home():
    bg_image_url = '/static/assets/img/home-bg.jpg'
    main_heading = 'Clean Blog'
    sub_heading = 'A Blog Theme by Start Bootstrap'
    blog_posts = BlogPost.query.all()
    return render_template('index.html', posts=blog_posts, bg_image_url=bg_image_url, main_heading=main_heading, sub_heading=sub_heading)

#--------------------------------------- Contacts #--------------------------------------- #
@app.route("/contact", methods=["GET", "POST"])
def contact():
    main_heading = 'Contact Me'
    sub_heading = 'Have questions? I have answers.'
    bg_image_url = '/static/assets/img/contact-bg.jpg'
    if request.method == "POST":
        data = request.form
        name = data['name']
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        sender_msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        send_email(sender_msg=sender_msg)
        return render_template("nav/contact.html", msg_sent=True, main_heading=main_heading, sub_heading=sub_heading, bg_image_url=bg_image_url)
    return render_template("nav/contact.html", msg_sent=False, main_heading=main_heading, sub_heading=sub_heading, bg_image_url=bg_image_url)

#--------------------------------------- About #--------------------------------------- #
@app.route('/about')
def about():
    main_heading = 'About Me'
    sub_heading = 'This is what I do.'
    bg_image_url = '/static/assets/img/about-bg.jpg'

    return render_template('nav/about.html', main_heading=main_heading, sub_heading=sub_heading, bg_image_url=bg_image_url)

#--------------------------------------- Manage Posts Route #--------------------------------------- #
@app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def blog(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()  # Create an instance of CommentForm

    if form.validate_on_submit():
        if current_user.is_authenticated:  # Ensure the user is authenticated
            new_comment = Comment(
                body=form.comment.data,
                post_id=blog_post.id,
                author_id=current_user.id  # Link the comment to the current user
            )
            db.session.add(new_comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')  # Optional flash message
            return redirect(url_for('blog', post_id=blog_post.id))  # Redirect back to the post

    # Fetch all comments for the blog post
    comments = Comment.query.filter_by(post_id=blog_post.id).all()
    comments_with_time_ago = [(comment, time_ago(comment.timestamp)) for comment in comments]
    return render_template('post.html', blog_post=blog_post, form=form, comments=comments_with_time_ago)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@app.route('/post', methods=['GET', 'POST'])  # For creating a new post
@login_required  
def manage_post(post_id=None):
    blog_post = BlogPost.query.get_or_404(post_id) if post_id else None
    form = PostForm(obj=blog_post)

    if form.validate_on_submit():
        if blog_post:  # Editing an existing post
            blog_post.title = form.title.data
            blog_post.subtitle = form.subtitle.data
            blog_post.date = form.date.data
            blog_post.body = form.body.data
            blog_post.img_url = form.img_url.data
            # Author should be set from the current user
            blog_post.author_id = current_user.id
        else:  # Creating a new post
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=form.date.data,
                body=form.body.data,
                author_id=current_user.id,  # Correctly set the author_id
                img_url=form.img_url.data
            )
            db.session.add(new_post)

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('manage_posts.html', form=form, blog_post=blog_post)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required  # Ensure only logged-in users can comment
def add_comment(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(
            body=form.comment.data,
            post_id=blog_post.id,
            author_id=current_user.id  # Assuming you want to link the comment to the current user
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('blog', post_id=blog_post.id))  # Redirect back to the post

    # If validation fails, redirect back (you could also flash an error message)
    return redirect(url_for('blog', post_id=blog_post.id))


@app.route("/delete/<int:post_id>")
@login_required  
def delete_post(post_id):
    post_to_delete = BlogPost.query.get_or_404(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

#--------------------------------------- Auth Route ---------------------------------------- #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    bg_image_url = 'https://brynfest.com/wp-content/uploads/2021/03/Factors-to-Consider-Before-Registering-a-Limited-Company.png'
    main_heading = 'Register'
    sub_heading = 'Create an account, share your articulate thoughts'
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            login_user(user)
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()  # Rollback the session on error
            flash('Email address already exists. Please use a different email.', 'danger')

    return render_template('nav/register.html', form=form, bg_image_url=bg_image_url, main_heading=main_heading, sub_heading=sub_heading)

@app.route('/login', methods=['GET', 'POST'])
def login():
    main_heading = 'Login'
    sub_heading = 'Access your account'
    bg_image_url = 'https://www.loginradius.com/blog/static/25f482319c5c4fcb1749a8c424a007b0/d3746/login-authentication.jpg'
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('nav/login.html', form=form, main_heading=main_heading, sub_heading=sub_heading, bg_image_url=bg_image_url)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))  # Redirect to login page if unauthorized

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

#--------------------------------------- Error Route ---------------------------------------- #
@app.errorhandler(404)
def not_found(error):
    return handle_4xx_error(404, "Sorry, the page you are looking for does not exist.")

@app.errorhandler(403)
def forbidden(error):
    return handle_4xx_error(403, "You do not have permission to access this page.")

@app.errorhandler(400)
def bad_request(error):
    return handle_4xx_error(400, "Bad request. Please check your input.")

def handle_4xx_error(code, message):
    return render_template('errors/4xx.html', code=code, message=message), code