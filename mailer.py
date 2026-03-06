import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime 
from flask import render_template
from config import Config
from models import db, Target

def build_email(target, campaign):
    tracking_url = f"{Config.BASE_URL}/track/{target.token}"
    html_body = render_template(f"email_templates/{campaign.template}.html", target_email=target.email, tracking_url=tracking_url, sender_name=Config.SENDER_NAME)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = get_subject_for_template(campaign.template)
    msg['From'] = f"{Config.SENDER_NAME} <{Config.SMTP_USERNAME}>"
    msg['To'] = target.email

    msg.attach(MIMEText(html_body, 'html'))
    return msg

def get_subject_for_template(template_name):
    subjects = {
        'password_reset': 'Important: Password Reset Required',
        'it_alert': 'IT SECURITY: Unusual login detected',
    }
    return subjects.get(template_name, 'Action Required')

def send_campaign_emails(campaign):
    try:
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)

        for target in campaign.targets:
            if not target.sent:
                msg = build_email(target, campaign)
                server.sendmail(Config.SMTP_USERNAME, target.email, msg.as_string())
                target.sent = True
                target.sent_at = datetime.utcnow()
                db.session.commit()
                print(f" ✅ Sent to {target.email}")

        server.quit()
        return True, "All emails sent successfully."
    
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP Authentication failed. Check your credentials."
    except smtplib.SMTPException as e:
        return False, f"An error occurred while sending emails: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"