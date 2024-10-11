from flask import Flask, render_template, request
import requests as rq
import smtplib

def send_email():
    with open (smtplib.SMTP('smtp.gmail.com',587)) as connection:
        connection.starttls()  # Secure the connection
        connection.login(username, password)  # Log in to the server
    

app = Flask(__name__)

@app.route('/')
def home():
    response = rq.get('https://api.npoint.io/674f5423f73deab1e9a7')
    blog_posts = response.json() #Type dict
    return render_template('index.html', posts=blog_posts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/form-entry", methods=['GET', 'POST'])
def receive_data():

    if request.method == 'POST':
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        return "<h1>Successfully sent your message</h1>"
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog/<int:post_id>')
def blog(post_id):
    response = rq.get('https://api.npoint.io/674f5423f73deab1e9a7')
    response.raise_for_status()
    blog_posts = response.json()  # Fetch again or cache it

    # Fetch the specific post
    blog_post = blog_posts[post_id]  # Assuming `post_id` matches the index in the list
    return render_template('post.html', blog_post=blog_post)



if __name__== "__main__":
    app.run(debug=True)