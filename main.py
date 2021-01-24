# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:35:51 2020

@author: Anant
"""


import keras
import matplotlib.pyplot as plt
from builtins import str
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
#from flask_mysqldb import MySQL
import numpy as np
from forms import ResetForm,RegistrationForm,LoginForm,EmptyForm,ForgotForm,NewPassForm,ChangePassword,fileform
import os
from flask_wtf.file import FileField,FileAllowed
from passlib.hash import pbkdf2_sha256
import sms
import random
from datetime import datetime,date
from math import ceil,floor,factorial
import math
import json
from bezier import evaluate_bezier
from sc import autocorrect
from azure_api_call import get_text

model=keras.models.load_model("DL-part/Model/model_74k_140.h5")

app = Flask(__name__)
#=============================================================================
#MYSQL CONFIGURATION
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'
app.secret_key='Nottobetold'
# app.config['UPLOAD_FOLDER']=PEOPLE_FOLDER
# app.config['CROP_IMG']=CROP_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Anant@1707'
app.config['MYSQL_DB'] = 'hwr'
mysql=MySQL(app)
#HOMEPAGE
char_map=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']


ii=np.array([i for i in range(62)])
def dataret(email):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='userinfo'")
    list1 = [a[0] for a in cursor.fetchall()]
    cursor.execute(f"SELECT * FROM userinfo where email='{email}'")
    dict1 = dict(zip(tuple(list1), cursor.fetchone()))
    return dict1

def show_first(y,l):
	result=""
	for i in range(l):
		if(y[i][0]>0.3):
			result+=(char_map[int(y[i][1])]+" ")
	return result

@app.route('/')
def home():
	form=EmptyForm()
	if(session.get('logged-in')):
		return redirect(url_for('userhome'))
	else:
		return render_template('index.html',form=form)

@app.route('/userhome')
def userhome():
    if(not session.get('logged-in')):
        flash('LOGIN to continue','danger')
        return redirect(url_for('login'))
    form=EmptyForm()
    return render_template('userhome.html',form=form,title="HOME")

@app.route('/RTHWR', methods=['GET','POST'])
def RTHWR():
    if(not session.get('logged-in')):
        flash('LOGIN first','danger')
        return redirect(url_for('login'))

    if(request.method=='POST'):
        resi=request.get_json(force=True)
        char_strokes=[]
        prevmaxx=-1
        prevminx=1300
        # for a character
        prev_stroke_set=[]
        first=False
       #for a sentence
        line=[]
        
        for stroke in resi:
            lst=[]
            
            for c in stroke:
                  lst.append([float(c['x']),float(c['y'])])
                
            StrokeSet=np.array(lst)
        
        
            minx = min(StrokeSet[:, 0])
           
            maxx = max(StrokeSet[:, 0])
            
          
            if((minx<prevmaxx and minx>prevminx  ) or(maxx>prevminx and maxx<prevmaxx)or(minx<prevminx and maxx>prevmaxx) or (minx>prevminx and maxx<prevmaxx)or (minx<prevminx and maxx>prevmaxx)):
                
                prev_stroke_set.append(StrokeSet)
                prevmaxx=max(maxx,prevmaxx)
               
                
                prevminx=min(minx,prevminx)
            else:
                first=True
                
                diff=minx-prevmaxx-50
                
                if(diff<0):
                    char_strokes.append(prev_stroke_set)
              
                    prev_stroke_set=[]
                    prev_stroke_set.append(StrokeSet)
                    prevmaxx=maxx
                    prevminx=minx
                else:
                    char_strokes.append(prev_stroke_set)
              
                    prev_stroke_set=[]
                    prev_stroke_set.append(StrokeSet)
                    prevmaxx=maxx
                    prevminx=minx
                    line.append(char_strokes)
                    char_strokes=[]
                    
                
                
        char_strokes.append(np.array(prev_stroke_set))
        line.append(char_strokes)
        char_strokes=0
        sentence=""
        for char_strokes in line:
            word=""
            
            for res in char_strokes:
                SS=[]
               
                for stroke in res:
                	lst=stroke
                	
                	SS.append(np.array(lst))
        
                sum=0
                sumi=0
                length=[]
                for i in SS:
                	length.append(len(i))
                	sum+=len(i)
        
                for i in range(len(length)):
                	length[i]=int((length[i]/sum)*140)
                	sumi+=length[i]
                sumi=sumi-length[-1]
        
                length[-1]=140-sumi
                # print(length)
                for i in range(len(length)):
                	SS[i]= evaluate_bezier(SS[i],length[i])
        
                lst=SS[0]
                for i in range(len(length)-1):
                 	lst=np.vstack((lst,SS[i+1]))
                
                StrokeSet=lst
        
                x,y=StrokeSet[:,0],StrokeSet[:,1]
        
                
                minx = min(StrokeSet[:, 0])
                miny = min(StrokeSet[:, 1])
                maxx = max(StrokeSet[:, 0])
                maxy = max(StrokeSet[:, 1])
                StrokeSet[:, 0] = StrokeSet[:, 0] - minx
                StrokeSet[:, 1] = StrokeSet[:, 1] - miny
    
                StrokeSet[:, 0] = StrokeSet[:, 0] / (maxx-minx)
                StrokeSet[:, 1] = StrokeSet[:, 1] / (maxy-miny)
    
    
           
                # print(StrokeSet.shape)
                StrokeSet=np.reshape(StrokeSet,(1,140,2))
    
    
    
                char_map=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']
    
            # x,y=StrokeSet[:,0],StrokeSet[:,1]
            # print("plotting started")
            # plt.plot(x, y, 'r.')
            # #plt.axis([0,1,1,0])
            # plt.savefig('plot.png')
            # plt.close()
            # print("plotting done")
            # # #print(StrokeSet)
                y=model.predict(StrokeSet)
                y=model.predict(StrokeSet)
    
                y=np.array(y)
                y=np.reshape(y,(62,))
                # print(y[np.argmax(y)]*100)
                word+=str(char_map[np.argmax(y)])	
            print(word)
            sentence+=autocorrect(word)
            sentence+=' '
            
        return (sentence)
        
        
    return render_template('splitup.html',title="Real Time Recognition")

@app.route('/WBO', methods=['GET','POST'])
def WBO():
    if(not session.get('logged-in')):
        flash('LOGIN first','danger')
        return redirect(url_for('login'))
    cursor=mysql.connection.cursor()

    #saving
    if request.method=='POST':
        res=request.get_json(force=True)

        foldername=session['email'].lower().split('@')
        foldername=foldername[0]+foldername[1][:-4]
        path=os.path.join(os.getcwd(),'static\\media\\wbd',foldername)


        if(not os.path.exists(path)):
            os.mkdir(path)

        drawing=dict()
        for i in range(len(res)-1):
            drawing[f"stroke{i}"]=res[i]
        
        filename=res[-1]['filename']
        print(filename)
        now=datetime.now()
        noww=now.strftime("%Y-%m-%d %H:%M:%S")
        with open(f'{path}/{filename}.json', 'w') as json_file:
            json.dump(drawing, json_file,indent=4)

        cursor.execute(f"select filename from wbd where filename='{filename}' and owned='{session['email'].lower()}'")
        a=cursor.fetchone()
        print(a)
        if a is None:
            cursor.execute(f"insert into wbd values('{session['email'].lower()}','{filename}','{noww}')")
        else:
            cursor.execute(f"update wbd set date_modified='{noww}' where owned='{session['email'].lower()}'")
    mysql.connection.commit()
        

    if(request.args.get('action')):
        action=request.args.get('action')
        if action=="create-new":
            return render_template("whiteboard.html")

        else:
            filename=request.args.get('filename')
            foldername=session['email'].split('@')
            foldername=foldername[0]+foldername[1][:-4]
            path=os.path.join(os.getcwd(),'static\\media\\wbd',foldername)
            

            if(action=='delete'):
                
                print(os.path.join(path,filename))
                if(os.path.exists(os.path.join(path,f"{filename}.json"))):
                    os.remove(os.path.join(path,f"{filename}.json"))
                    cursor.execute(f"delete from wbd where owned='{session['email'].lower()}' and filename='{filename}'")
                    mysql.connection.commit()
                    return redirect(url_for('WBO'))
            if(action=='open'):
                    with open(f"{path}/{filename}.json") as f:
                        data=json.load(f)
                    points=[]
                    for key,value in data.items():
                        stroke=value
         
                        points.append(stroke)

                    print(points)
                    return render_template('whiteboard.html',data=points)
    
    cursor.execute(f"select * from wbd where owned='{session['email'].lower()}' order by date_modified desc")
    a=cursor.fetchall()
    #print(a)
    foldername=session['email'].lower().split('@')
    foldername=foldername[0]+foldername[1][:-4]
    path=f"media/wbd/{foldername}"
    return render_template('wbohead.html',form=EmptyForm(),title="Whiteboard",d=a,path=path)
    
@app.route('/uploadpdf', methods=['GET','POST'])
def uploadpdf():
    form=fileform()
    if(not session.get('logged-in')):
        flash('LOGIN first','danger')
        return redirect(url_for('login'))
    if request.method=='POST':
        file=request.files['pdfile']
        output=get_text(file)
        return render_template('output.html',output=output)
    return render_template('uploadpdf.html',form=form,title="Convert from File")

@app.route('/register',methods=['GET','POST'])
def register():
    session.pop('logged-in',False)
    form=RegistrationForm()
    if request.method=='POST':
        if form.validate_on_submit():
            cursor=mysql.connection.cursor()
            result=request.form.to_dict()
            result['email']=form.data['email'].lower()

            regdata=[]

            for key,value in result.items():
                if(key=='submit' or key=='cpassword' or key=='csrf_token'):
                    continue
                elif (key=='password'):
                    regdata.append(pbkdf2_sha256.hash(value))
                elif(key!='type'):
                    regdata.append(value)
            #fname,lname,phone,email,password
            #print(f"INSERT INTO USERINFO VALUES {tuple(regdata)}")

            try:
                #print(f"INSERT INTO USERINFO VALUES {tuple(regdata)}")
                cursor.execute(f"INSERT INTO USERINFO VALUES {tuple(regdata)}")

            except:
                flash('Some Error Occured,Try Again!','danger')
                return redirect(url_for('register'))

            mysql.connection.commit()
            cursor.close()
            session['log-in']='reg'
            session['phone'] = result['phone']
            flash("Verify Otp!","info")
            return redirect(url_for('resetpass'))
                
        else:
            return render_template('register.html',form=form)
    else:
        return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    session.pop('logged-in',False)
    form=LoginForm()
    if(request.method == 'POST'):
        cursor=mysql.connection.cursor()
        result=form.data
        cursor.execute(f"Select passwordd from userinfo where lower(email)='{result['email'].lower()}'")
        a=cursor.fetchone()
        if a is None:
            flash(f"NO ACCOUNT EXISTS WITH THIS USERNAME",'danger')
            return redirect(url_for('register'))
        else:
            dict1 = dataret(result['email'].lower())
            if pbkdf2_sha256.verify(result['password'], a[0]):
                session['logged-in']=True
                session['email']=result['email']
                return redirect(url_for('userhome'))

            else:
                flash("Incorrect Password!","danger")
                return render_template("login.html",form=form)
    else:

        return render_template('login.html',form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    session.pop('logged-in', False)
    form=ForgotForm()
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        phone=form.data['phone']
        cursor.execute(f"select email from userinfo where phone = '{phone}' ")
        a=cursor.fetchone()
        if(a == None):
            flash("You are not registered!!,REGISTER NOW", 'danger')
            return redirect(url_for('register'))
        else:
            session['phone'] = phone
            session['logged-in']=False
            session['email']=a[0]
            return redirect(url_for('resetpass'))

    return render_template('forgot.html',form=form)

@app.route('/reset', methods=['GET', 'POST'])
def resetpass():
    if(not session.get('phone')):
        flash('Restricted','danger')
        return redirect(url_for('login'))

    form= ResetForm()
    if request.method == 'POST':
        ootp = form.data['otp']
        if ootp == session['otp']:
            if(session.get('log-in')=='reg'):

                mysql.connection.commit()
                session.pop('log-in', None)
                session.pop('phone', None)

                return redirect(url_for('login'))




            return redirect(url_for('newpass'))
        else:

            flash('INVALID OTP', 'danger')
            return redirect(url_for('resetpass'))


    otp1 = str(random.randrange(100000, 999999))
    print(otp1)
    URL = 'https://www.way2sms.com/api/v1/sendCampaign'
    session['otp']=otp1
    phone=session['phone']

    #resp=sms.sendPostRequest(URL, 'C23FTIDPYUYZVP7UV238S0QC1POBFWMR', 'N1AY9Q2S52NHUADE', 'stage', phone, '9781396442', f"Your OTP (One Time Password) to change your password is: {otp1} Do not share this with anyone!   Team college+")
    #print(resp.text)
    return render_template('verifyotp.html',form=form)

@app.route('/changepass',methods=['GET','POST'])
def changepass():
    if (not session.get('logged-in')):
        flash('LOGIN TO CONTINUE', 'danger')
        return redirect(url_for('logout'))

    form=ChangePassword()
    if request.method=='POST':
        if form.is_submitted():
            oldp=form.oldpassword.data
            dict1=dataret(session['email'])
            if pbkdf2_sha256.verify(oldp,dict1['passwordd']):
                cursor=mysql.connection.cursor()
                newpassworda=pbkdf2_sha256.hash(form.password.data)
                cursor.execute(f" UPDATE  userinfo  set passwordd = '{newpassworda}' where email='{session['email']}' ")
                mysql.connection.commit()
                flash('Update successfull', 'success')
                return redirect(url_for('userhome'))
            else:
                flash('Enter Correct old password', 'danger')
                return redirect(url_for('changepass'))

    return render_template('newpass.html',form=form,title="Change Password")

@app.route('/newpass', methods=['GET', 'POST'])
def newpass():
    form=NewPassForm()
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        newpassword = form.data['password']
        confirmnewpassword = form.data['cpassword']

        if (newpassword == confirmnewpassword):
            newpassworda = pbkdf2_sha256.hash(newpassword)

            cursor.execute(f" UPDATE  userinfo  set passwordd = '{newpassworda}' where email =  '{session['email']}' ")
            mysql.connection.commit()
            session['logged-in']=True
            return redirect(url_for('home'))
        else:
            flash("passwords didnt match", 'danger')
            return redirect(url_for('newpass'))
    return render_template('newpass.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    session.pop('logged-in', False)
    session.pop('phone', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)