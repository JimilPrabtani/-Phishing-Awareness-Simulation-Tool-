import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY' , 'change-me-in-production')

    #database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///philips_sim.db'

    #SMTP Settings - use a dedicated test mailbox for development!
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')

    SENDER_NAME = os.environ.get('SENDER_NAME', 'IT Security Team')

    #Base URL for tracking links
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')