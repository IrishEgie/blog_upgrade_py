import os
import smtplib
from datetime import datetime, timedelta

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
