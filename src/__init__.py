from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler


# from database.create_db import create_database
db = SQLAlchemy()
DB_NAME = "future_career.db"
scheduler = APScheduler()

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

    @login_manger.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    scheduler.init_app(app)
    scheduler.start()
    
    return app
