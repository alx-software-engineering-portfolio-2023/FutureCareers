from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail)
import os
from datetime import date, timedelta 

scheduler = APScheduler()

# from database.create_db import create_database
db = SQLAlchemy()
DB_NAME = "future_career.db"


def SendEMail(email, content):
    message = Mail(
    from_email='futurecareersalx@gmail.com',
    to_emails=email,
    subject="Don't forget to apply",
    html_content='<strong>These jobs close tomorrow</strong><br>' + content)
    try:
        sg = SendGridAPIClient(os.getenv("FUTURECAREERS_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


@scheduler.task('cron', id='send_notification', minute='59')
def SendNotification():
    from src.models.models import User, Saved
    with scheduler.app.app_context():
        mail_list = {}
        closing_tomorrow = date.today() + timedelta(days=1)
        jobs = Saved.query.filter_by(closing_date=closing_tomorrow)
        for job in jobs:
            if job.user_id not in mail_list.keys():
                mail_list[job.user_id] = [f'<a href="{job.link}">{job.job_title}</a>']
            else:
                temp = mail_list[job.user_id]
                temp.append(f'<a href="{job.link}">{job.job_title}</a>')
                #mail_list[job.user_id] = temp
        for key, value in mail_list.items():
            email = User.query.filter_by(id=key).first().email
            SendEMail(email, "\n".join(value))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Master_of_Mystic_Arts'
    
    # Create Database and Intitialize the Database
    # Create_database(DB_NAME)
    
    # To use MySQL Database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{os.getenv("AZURE_MYSQL_USER")}:{os.getenv("AZURE_MYSQL_PASSWORD")}@{os.getenv("AZURE_MYSQL_HOST")}/{os.getenv("AZURE_MYSQL_NAME")}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from src.views.admin_routes import admin
    from src.views.auth_routes import auth
    from src.views.member_routes import member
    from src.views.public_routes import public
    
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(member, url_prefix='/member')
    app.register_blueprint(public, url_prefix='/')
    
    from src.models.models import User, Saved
    
    with app.app_context():
        db.create_all()
        
    login_manger = LoginManager()
    login_manger.login_view = 'auth.login'
    login_manger.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    @login_manger.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
