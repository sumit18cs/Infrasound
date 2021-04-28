from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from kombu.utils.url import safequote


application = Flask(__name__)
ALLOWED_EXTENSIONS = {'mp4'}

application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True


db=SQLAlchemy(application)
bcrypt =Bcrypt(application)
login_manager=LoginManager(application)
login_manager.login_view='login' #setting the route to login
login_manager.login_message_category='info'
application.config['MAIL_SERVER']='smtp.googlemail.com'
application.config['MAIL_USE_TLS']=587
application.config['MAIL_USERNAME']='sumit.11.sky@gmail.com'
application.config['MAIL_PASSWORD']='password'
mail=Mail(application)
from THAT import routes