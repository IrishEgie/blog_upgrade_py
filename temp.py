import requests as rq
import smtplib
import os

user_email = os.getenv('EMAIL')
user_pass = os.getenv('PASSWORD')
def send_email(sender_msg=''):
    try:
        # Use a context manager for the SMTP connection
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()  # Secure the connection
            connection.login(user=user_email, password=user_pass)   # Log in to the server

            # Send the email
            connection.sendmail(from_addr=user_email, to_addrs=os.getenv('SENDEE'), msg=sender_msg)
            print('Email sent successfully!')

    except Exception as e:
        print(f'Failed to send email: {e}')


send_email(sender_msg='Trial if email & pass works for smtp')