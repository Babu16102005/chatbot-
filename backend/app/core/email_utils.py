import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
def send_otp_email(to_email: str, otp: str):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        print('SMTP not configured — OTP:', otp)
        return
    msg = EmailMessage()
    msg['Subject'] = 'Career ChatBot OTP'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.set_content(f'Your OTP: {otp}. Expires in 10 minutes.')
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
