import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


def send_mail(student, instructor, cohort_name, rating, comments):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    login = os.getenv('login')
    password = os.getenv('password')
    message = f"<h3>New Feedback Submission Received</h3><ul><li>Student Name: {student}</li><li>Instructor Name: {instructor}" \
              f"</li><li>Cohort Name: {cohort_name}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'TwinsCodingCamp Students Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
