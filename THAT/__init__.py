from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from kombu.utils.url import safequote


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'mp4'}

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True


db=SQLAlchemy(app)
bcrypt =Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login' #setting the route to login
login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_USE_TLS']=587
app.config['MAIL_USERNAME']='sumit.11.sky@gmail.com'
app.config['MAIL_PASSWORD']='password'
mail=Mail(app)
from THAT import routes
