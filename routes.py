from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from app import app, db, login_manager
from models import BlogPost, User
from forms import PostForm, RegistrationForm
from email_utils import send_email
from werkzeug.security import check_password_hash 
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
    if request.method == "POST":
        data = request.form
        name = data['name']
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        sender_msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        send_email(sender_msg=sender_msg)
        return render_template("nav/contact.html", msg_sent=True)
    return render_template("nav/contact.html", msg_sent=False)

#--------------------------------------- About #--------------------------------------- #
@app.route('/about')
def about():
    return render_template('nav/about.html')

#--------------------------------------- Manage Posts Route #--------------------------------------- #
@app.route('/blog/<int:post_id>')
def blog(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', blog_post=blog_post)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@app.route('/post', methods=['GET', 'POST'])  # For creating a new post
def manage_post(post_id=None):
    blog_post = BlogPost.query.get_or_404(post_id) if post_id else None
    form = PostForm(obj=blog_post)

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
        return redirect(url_for('home'))

    return render_template('manage_posts.html', form=form, blog_post=blog_post)

@app.route("/delete/<int:post_id>")
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
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('home'))
    return render_template('nav/register.html', form=form, bg_image_url=bg_image_url, main_heading=main_heading, sub_heading=sub_heading)

@app.route('/login', methods=['GET', 'POST'])
def login():
    main_heading = 'Login'
    sub_heading = 'Access your account'
    bg_image_url = 'https://www.loginradius.com/blog/static/25f482319c5c4fcb1749a8c424a007b0/d3746/login-authentication.jpg'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('nav/login.html', main_heading=main_heading, sub_heading=sub_heading,  bg_image_url=bg_image_url)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')
