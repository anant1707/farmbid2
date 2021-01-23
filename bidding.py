from builtins import str
#import generate
from flask import Flask,render_template,request,redirect,url_for,flash,session
#import psycopg2 as psql
#import mail
#import pandas as pd
#import numpy as np
from forms import ResetForm,payment,RegistrationForm,LoginForm,EmptyForm,AcceptBidForm,UpdateForm,ForgotForm,NewPassForm,ImgForm,ChangePassword,CropUploadForm,AddCropForm,basepriceForm,SearchForm,ViewCropForm
import os
from flask_wtf.file import FileField,FileAllowed
#from passlib.hash import pbkdf2_sha256
#import sms
#import random
#from datetime import date
#import pickle
#import numpy as np
#import shutil
#import datetime



PEOPLE_FOLDER=os.path.join('static','media/profile_image')
CROP_FOLDER=os.path.join('static','media/cropimg')
a=[["Cotton","1250","Punjab"],["Wheat","1500","Punjab"],["Rice","1800","Punjab"],["Corn","1000","Punjab"]]

app=Flask(__name__)
app.secret_key='Nottobetold'
app.config['UPLOAD_FOLDER']=PEOPLE_FOLDER
app.config['CROP_IMG']=CROP_FOLDER



@app.route('/')
def home():
    if(session.get('logged-in')):
        return redirect(url_for('userhome'))

    form=EmptyForm()
    return render_template('index.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    session.pop('logged-in',False)
    session.pop('phone',False)
    form=LoginForm()
    if(request.method == 'POST'):
        #cursor=conn.cursor()
        result=form.data
        session['logged-in']=True
        session['email']=result['email'][:10]
        session['trueemail']=result['email']
        return redirect(url_for('userhome'))
    return render_template('login.html',form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    session.pop('logged-in', False)

    return redirect(url_for('home'))

@app.route('/userhome',methods=['GET','POST'])
def userhome():
    if (not session.get('logged-in')):
        flash('LOGIN TO CONTINUE', 'danger')
        return redirect(url_for('logout'))
    form=SearchForm()
    dict1=[]

    return render_template('bhome.html', form=form, b=a, dict1=dict1)

@app.route('/profile',methods=['GET','POST'])
def profile():
    if (not session.get('logged-in')):
        flash('LOGIN TO CONTINUE','danger')
        return redirect(url_for('logout'))

    form=EmptyForm()

    return render_template('profile.html',form=form)

@app.route('/viewcrop',methods=['GET','POST'])
def viewcrop():
    return redirect(url_for('userhome'))

@app.route('/addtocart',methods=['GET','POST'])
def addtocart():
    return redirect(url_for('userhome'))



if(__name__== '__main__'):
        app.run(host="192.168.0.103",debug=True)



"""

files = ['file1.txt', 'file2.txt', 'file3.txt']
for f in files:
    shutil.copy(f, 'dest_folder')
os.remove(path)
rename(fname, fname.replace(name, '', 1))

"""
