from flask import render_template, url_for, flash, redirect,request,abort,jsonify,session
import requests
import json
import imaplib
from THAT import app,db,bcrypt,mail #using bcrypt to has the passwords in user database
from THAT.models import User, Lecture, Skill, Sign
from THAT.forms import RegistrationForm, LoginForm,LectureForm,SearchForm,MessageForm,UpdateAccountForm,FeedbackForm,ReadingForm
from flask_login import login_user,current_user,logout_user,login_required
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime, timedelta
from random import sample
from THAT.search import KMPSearch

import urllib.request
import urllib.parse
from flask_mail import Message

#--------------------------------------------------------------------------------------------
import time
import string
# import pyaudio
import speech_recognition as sr
from plyer import notification 
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from THAT.features import getRoS, getTranscript
#--------------------------------------------------------------------------------------------

import os
from os import path
import moviepy.editor as mp

#--------------------------------------------------------------------------------------------
#everything here that begins with @ is a decorator
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])

@app.route("/home")
def home():
    return render_template('home.html',db=db,User=User,Lecture=Lecture)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))  
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')#looks for queries in request; args is a dictionary; we use get and not directly use 'next' as key to return the value because key might be empty leading to an error. get, in that case would fetch a none
            flash('Greetings '+form.username.data+' !','success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    skills = Skill.query.filter_by(author=current_user)
    e=0
    m=0
    h=0
    w=0
    for skill in skills:
        if skill.done == 1:
            if skill.difficulty == 1:
                e=e+1
            elif skill.difficulty ==2:
                m=m+1
            else:
                h=h+1
        elif skill.done == 2:
            w=w+1

    signs = Sign.query.filter_by(author=current_user)
    e1=0
    m1=0
    h1=0
    w1=0
    for sign in signs:
        if sign.done == 1:
            if sign.difficulty == 1:
                e1=e1+1
            elif sign.difficulty ==2:
                m1=m1+1
            else:
                h1=h1+1
        elif sign.done == 2:
            w1=w1+1
    return render_template('dashboard.html', title='Dashboard',e=e,m=m,h=h,w=w,e1=e1,m1=m1,h1=h1,w1=w1)

@app.route("/about", methods=['GET', 'POST'])
@login_required
def about():
    return render_template('about.html', title='About')
    
@app.route("/tutorial", methods=['GET', 'POST'])
@login_required
def tutorial():
    skills = Skill.query.filter_by(author=current_user)
    e=0
    m=0
    h=0
    w=0
    for skill in skills:
        if skill.done == 1:
            if skill.difficulty == 1:
                e=e+1
            elif skill.difficulty ==2:
                m=m+1
            else:
                h=h+1
        elif skill.done == 2:
            w=w+1

    users=User.query.all()
    total=len(users)
    
    skills=Skill.query.all()
    ans = [0] * 17
    for skill in skills:
        if skill.done == 1:
            ans[skill.video_id] = ans[skill.video_id] + 1
    
    print(ans)
    return render_template('tutorial.html', title='Lip Reading',e=e,m=m,h=h,w=w,total=total,ans=ans)


@app.route("/lipreading/<int:video_id>", methods=['GET', 'POST'])
@login_required
def lipreading(video_id):
    print(video_id)
    video=Skill.query.get_or_404(video_id)
    a=video.title
    print(a)
    print(len(a))
    hint=len(a)
    form=ReadingForm() 
    username=current_user.username
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        skills=Skill.query.filter_by(author=current_user)
        for skill in skills:
            if int(skill.video_id) == int(video_id):
                if skill.title == form.search.data :
                    print('yooo')
                    skill.done=1
                    db.session.commit()
                    flash(f'Correct Answer !!','success')
                    return redirect(url_for('tutorial')) 

                if skill.done != 1:
                    skill.done=2
                    db.session.commit()            
                    flash(f'Incorrect Answer !!','danger')
                    return redirect(url_for('lipreading',video_id=video_id)) 
        flash(f'Incorrect Answer !!','danger')
        return redirect(url_for('lipreading',video_id=video_id)) 
    return render_template('lipreading.html', title='Lip Reading',form=form,video_id=video_id,hint=hint)

@app.route("/sign_tutorial", methods=['GET', 'POST'])
@login_required
def sign_tutorial():
    signs = Sign.query.filter_by(author=current_user)
    e=0
    m=0
    h=0
    w=0
    for sign in signs:
        if sign.done == 1:
            if sign.difficulty == 1:
                e=e+1
            elif sign.difficulty ==2:
                m=m+1
            else:
                h=h+1
        elif sign.done == 2:
            w=w+1

    users=User.query.all()
    total=len(users)
    
    signs=Sign.query.all()
    ans = [0] * 17
    for sign in signs:
        if sign.done == 1:
            ans[sign.video_id] = ans[sign.video_id] + 1
    
    print(ans)
    return render_template('sign_tutorial.html', title='Sign Reading',e=e,m=m,h=h,w=w,total=total,ans=ans)


@app.route("/signreading/<int:video_id>", methods=['GET', 'POST'])
@login_required
def signreading(video_id):
    print(video_id)
    video=Sign.query.get_or_404(video_id)
    a=video.title
    print(a)
    print(len(a))
    hint=len(a)
    form=ReadingForm() 
    username=current_user.username
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        signs=Sign.query.filter_by(author=current_user)
        for sign in signs:
            if int(sign.video_id) == int(video_id):
                if sign.title == form.search.data :
                    print('yooo')
                    sign.done=1
                    db.session.commit()
                    flash(f'Correct Answer !!','success')
                    return redirect(url_for('sign_tutorial')) 

                if sign.done != 1:
                    sign.done=2
                    db.session.commit()            
                    flash(f'Incorrect Answer !!','danger')
                    return redirect(url_for('signreading',video_id=video_id)) 
        flash(f'Incorrect Answer !!','danger')
        return redirect(url_for('signreading',video_id=video_id)) 
    return render_template('signreading.html', title='Sign Reading',form=form,video_id=video_id,hint=hint)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard')) #redirects user to dashboard if already logged in; function name is passed in url_for
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8') #returns hashed password, decode converts it from byte to string
        #if app_password field is not-empty
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)

        db.session.add(user)
        db.session.commit()
        user=User.query.filter_by(username=form.username.data).first()
        print(user.username)
        print(user.id)  
              
        video_reading = { 1:'ball' , 2:'dad' , 3:'blue' , 4:'the' , 5:'three' }
        for item, value in video_reading.items():
            skill=Skill(title=value,video_id=item,user_id=user.id,difficulty=1)
            db.session.add(skill)
            db.session.commit()

        video_reading = { 6:'bus' , 7:'will' , 8:'mom' , 9:'fast' , 10:'five' , 11:'laugh' }
        for item, value in video_reading.items():
            skill=Skill(title=value,video_id=item,user_id=user.id,difficulty=2)
            db.session.add(skill)
            db.session.commit()

        video_reading = { 12:'ten' , 13:'me' , 14:'two' , 15:'you' , 16:'please'}
        for item, value in video_reading.items():
            skill=Skill(title=value,video_id=item,user_id=user.id,difficulty=3)
            db.session.add(skill)
            db.session.commit()

        # sign reading
        video_reading = { 1:'six' , 2:'four' , 3:'seven' , 4:'five' , 5:'nine' }
        for item, value in video_reading.items():
            sign=Sign(title=value,video_id=item,user_id=user.id,difficulty=1)
            db.session.add(sign)
            db.session.commit()

        video_reading = { 6:'ten' , 7:'eight' , 8:'orange' , 9:'blue' , 10:'yellow'}
        for item, value in video_reading.items():
            sign=Sign(title=value,video_id=item,user_id=user.id,difficulty=2)
            db.session.add(sign)
            db.session.commit()

        video_reading = { 11:'animals' , 12:'cat' , 13:'bird' , 14:'bat' , 15:'bear' , 16:'alligator'}
        for item, value in video_reading.items():
            sign=Sign(title=value,video_id=item,user_id=user.id,difficulty=3)
            db.session.add(sign)
            db.session.commit()


        flash(f'You have successfully registered.', 'success')
        return redirect(url_for('login'))
    image_file=url_for('static',filename='images/user.png')

    return render_template('register.html', title='Register', image_file=image_file,form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    image_file=url_for('static',filename='images/user.png')
    return render_template('account.html',title='Account',image_file=image_file)

@app.route("/account/update",methods=['GET', 'POST'])
@login_required
def update_account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
       # hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8') #returns hashed password, decode converts it from byte to string
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Account updated successfully!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':  #if submit btn is not clicked and account page is requested, it eill already fill the usename field with existing data
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('update_account.html',title='Update Account',image_file=image_file,form=form,legend='Update credentials')

@app.route("/account/delete",methods=['GET', 'POST'])
@login_required
def delete_account():
    user=User.query.filter_by(id=current_user.id).first()
    lectures=Lecture.query.filter_by(user_id=current_user.id).all()
    for lecture in lectures:
        db.session.delete(lecture)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted','success')
    return redirect(url_for('register'))

@app.route("/contact_us",methods=['GET', 'POST'])
def contact_us():
    form=MessageForm()
    if current_user.is_authenticated:
        form.email.data=current_user.email
    if form.validate_on_submit():
        msg=Message('Sent by THAT user: '+current_user.username,sender=form.email.data,recipients=['that.admn@gmail.com']) 
        msg.body=f'''Sent from THAT contact us page:
        {form.message.data}'''
        mail.send(msg)
        flash('Your message has been sent.','success')
    return render_template("contact_us.html",form=form)

@app.route("/speechAsisstance",methods=['GET', 'POST'])
def speechAsisstance():
    return render_template("speechAsisstance.html") 


@app.route("/speechAsisstance_RoS")
def speechAsisstance_RoS():
    print("Starting Recording\n")
    average_RoS, words_in_speech, text = getRoS()
    string3 = str(words_in_speech) + " words"
    string4 = str(average_RoS) + " words/min" 
    message1 = "<h3>" +str(average_RoS) + " words/min</h3>" 
    message2 = "<h5 class=\"mb-6\">You said        : <span class=\"text-muted h5 font-weight-normal\">" + text + "<br></span></h5>"
    message3 = "<h5 class=\"mb-6\">Words in Speech : <span class=\"text-muted h5 font-weight-normal\">" + string3 + "<br></></h5>"
    message4 = "<h5 class=\"mb-6\">Rate of Speech  : <span class=\"text-muted h5 font-weight-normal\">" + string4 + "<br></></h5>"
    
    ret_val = jsonify(message1 =message1, message2= message2 ,message3=message3,message4=message4)
    return ret_val

@app.route("/transcripts",methods=['GET', 'POST'])
def transcripts():
    return render_template("transcripts.html") 

@app.route("/getranscripts",methods=['GET', 'POST'])
def getranscripts():
    #path = path of current_lecture
    path = "C:/Users/Dell/Desktop/t4sne/Codes/THAT/static/video/video_transcript.mp4"
    transcript = getTranscript(path)
    transcript ="<h4 id =\"Transcripts\" style=\"font-size: medium;font-family: 'Courier New', Courier, monospace;\">" + str(transcript) + "</h4>"  
    ret_val = jsonify(message = transcript)
    return ret_val

@app.route("/video_player/ <int:lecture_id>")
@login_required
def video_player(lecture_id):
    lecture=Lecture.query.get_or_404(lecture_id) #get_or_404 returns the requested page if it exists else it returns a 404 error
    return render_template('video_player.html',title=lecture.title,lecture=lecture)

    
@app.route("/video_transcripts",methods=['GET', 'POST'])
@login_required
def video_transcripts():
    return render_template('video_transcripts.html')
