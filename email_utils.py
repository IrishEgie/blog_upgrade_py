import os
import smtplib

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
