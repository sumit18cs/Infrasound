from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from THAT import db,login_manager,application
from flask_login import UserMixin

#decorator for login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #getting user by id


class User(db.Model, UserMixin):
    #__tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True, nullable=False)
    email=db.Column(db.String(100),unique=True, nullable=False)
    password=db.Column(db.String(50),nullable=False)
    user_type=db.Column(db.String(20), nullable=False,default='Student') #student or professor
    lectures=db.relationship('Lecture',backref='author',lazy=True)
    image_file=db.Column(db.String(20),nullable=False,default='user.png')
    skills = db.relationship('Skill', backref='author', lazy=True)
    signs = db.relationship('Sign', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id=db.Column(db.Integer)
    done = db.Column(db.Integer, default=0)
    title = db.Column(db.String(200), nullable=False)
    difficulty=db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Skill('{self.title}', '{self.done}')"


class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id=db.Column(db.Integer)
    done = db.Column(db.Integer, default=0)
    title = db.Column(db.String(200), nullable=False)
    difficulty=db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Sign('{self.title}', '{self.done}')"


class Lecture(db.Model):
    #__tablename__ = "lectures"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date=db.Column(db.Date(),nullable=False)
    starttime=db.Column(db.Time,nullable=True)
    endtime=db.Column(db.Time,nullable=True)
    details=db.Column(db.Text,nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    video_path=db.Column(db.String(100),nullable=True,default='video/1.mp4')
    video_transcript=db.Column(db.Text,nullable=True)    
    def __repr__(self):
        return f"Lecture('{self.title}','{self.date}','{self.starttime}','{self.endtime}')"

