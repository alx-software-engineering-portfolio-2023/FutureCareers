from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail)
import os

scheduler = APScheduler()

# from database.create_db import create_database
db = SQLAlchemy()
DB_NAME = "future_career.db"


def SendEMail(email, content):
    message = Mail(
    from_email='futurecareersalx@gmail.com',
    to_emails=email,
    subject='Your Jobs list',
    html_content=content)
    try:
        sg = SendGridAPIClient(os.getenv("FUTURECAREERS_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


@scheduler.task('cron', id='send_notification', minute='19')
def SendNotification():
    from models.models import User, Saved
    with scheduler.app.app_context():
        mail_list = {}
        jobs = Saved.query.all()#.filter_by() date 1 day before closing
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
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://username:password@localhost/db_name'
    # app.config[
        # 'SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://root:Legend1240s26#@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from views.admin_routes import admin
    from views.auth_routes import auth
    from views.member_routes import member
    from views.public_routes import public
    
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(member, url_prefix='/member')
    app.register_blueprint(public, url_prefix='/')
    
    from models.models import User, Saved
    
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
