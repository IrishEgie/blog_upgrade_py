from flask import Flask, render_template, request
import requests as rq
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

@app.route('/')
def home():
    response = rq.get('https://api.npoint.io/674f5423f73deab1e9a7')
    blog_posts = response.json() #Type dict
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
    response = rq.get('https://api.npoint.io/674f5423f73deab1e9a7')
    response.raise_for_status()
    blog_posts = response.json()  # Fetch again or cache it

    # Fetch the specific post
    blog_post = blog_posts[post_id]  # Assuming `post_id` matches the index in the list
    return render_template('post.html', blog_post=blog_post)



if __name__== "__main__":
    app.run(debug=True)