from builtins import str
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify,make_response,send_from_directory
import pyodbc
from forms import ResetForm,RegistrationForm,LoginForm,EmptyForm,ForgotForm,NewPassForm,ChangePassword,NotificationForm
import os
from flask_wtf.file import FileField,FileAllowed
from passlib.hash import pbkdf2_sha256
import random
from datetime import datetime,date
import math
import json
import mail


app = Flask(__name__)
#=============================================================================
#MYSQL CONFIGURATION
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'
server = 'anant.database.windows.net'
database = 'hwr'
username = 'root7'
password = 'Anant@1707'
driver= 'ODBC Driver 17 for SQL Server'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


def dataret(email):
    cursor=cnxn.cursor()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='userinfo'")
    list1 = [a[0] for a in cursor.fetchall()]
    cursor.execute(f"SELECT * FROM userinfo where email='{email}'")
    dict1 = dict(zip(tuple(list1), cursor.fetchone()))
    return dict1

@app.route('/sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',filename='sw.js'))
    #change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    return response
    
@app.route('/')
def home():
	form=EmptyForm()
	if(session.get('logged-in')):
		return redirect(url_for('userhome'))
	else:
		return render_template('index.html',form=form)

@app.route('/admin',methods=['GET','POST'])
def admin():
    form=NotificationForm()
    if request.method=='POST':
        if form.is_submitted():
            nf=form.data['notification']
            return render_template('help.html',nf=f"{nf}")
    return render_template('admin.html',form=form)

@app.route('/userhome')
def userhome():
    if(not session.get('logged-in')):
        flash('LOGIN to continue','danger')
        return redirect(url_for('login'))
    form=EmptyForm()
    return render_template('userhome.html',form=form,title="HOME")

@app.route('/WBO', methods=['GET','POST'])
def WBO():
    if(not session.get('logged-in')):
        flash('LOGIN first','danger')
        return redirect(url_for('login'))
    cursor=cnxn.cursor()

    #saving
    if request.method=='POST':
        res=request.get_json(force=True)
        foldername=session['email'].lower().split('@')
        foldername=foldername[0]+foldername[1][:-4]
        path=os.path.join(app.root_path,f'static/media/wbd/{foldername}')
        
        drawing=dict()
        for i in range(len(res)-1):
            drawing[f"stroke{i}"]=res[i]
        
        filename=res[-1]['filename']
        
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

        cnxn.commit()
        

    if(request.args.get('action')):
        action=request.args.get('action')
        if action=="create-new":
            return render_template("whiteboard.html")

        else:
            filename=request.args.get('filename')
            foldername=session['email'].split('@')
            foldername=foldername[0]+foldername[1][:-4]
            path=os.path.join(app.root_path,f'static/media/wbd/{foldername}')
            

            if(action=='delete'):
                
                #print(os.path.join(path,filename))
                if(os.path.exists(os.path.join(path,f"{filename}.json"))):
                    os.remove(os.path.join(path,f"{filename}.json"))
                    cursor.execute(f"delete from wbd where owned='{session['email'].lower()}' and filename='{filename}'")
                    cnxn.commit()
                    return redirect(url_for('WBO'))
            if(action=='open'):
                    with open(f"{path}/{filename}.json") as f:
                        data=json.load(f)
                    points=[]
                    for key,value in data.items():
                        stroke=value
         
                        points.append(stroke)

                    #print(points)
                    return render_template('whiteboard.html',data=points)
    
    cursor.execute(f"select * from wbd where owned='{session['email'].lower()}' order by date_modified desc")
    a=cursor.fetchall()
    #print(a)
    foldername=session['email'].lower().split('@')
    foldername=foldername[0]+foldername[1][:-4]
    path=f"media/wbd/{foldername}"
    return render_template('wbohead.html',form=EmptyForm(),title="Whiteboard",d=a,path=path)
    
@app.route('/register',methods=['GET','POST'])
def register():
    session.pop('logged-in',False)
    form=RegistrationForm()
    if request.method=='POST':
        if form.validate_on_submit():
            cursor=cnxn.cursor()
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
                session['email']=result['email']
                foldername=session['email'].lower().split('@')
                foldername=foldername[0]+foldername[1][:-4]
                os.mkdir(os.path.join(app.root_path,f'static/media/wbd/{foldername}'))

            except:
                flash('Some Error Occured,Try Again!','danger')
                return redirect(url_for('register'))

            cnxn.commit()
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
        cursor=cnxn.cursor()
        result=form.data

        if(result['email']=="admin" and result['password']=="1234"):
            return redirect(url_for('admin'))
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
    cursor = cnxn.cursor()
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

                cnxn.commit()
                session.pop('log-in', None)
                session.pop('phone', None)

                return redirect(url_for('login'))

            return redirect(url_for('newpass'))
        else:

            flash('INVALID OTP', 'danger')
            return redirect(url_for('resetpass'))


    otp1 = str(random.randrange(100000, 999999))
    print(otp1)
    #URL = 'https://www.way2sms.com/api/v1/sendCampaign'
    session['otp']=otp1
    mail.sendmail(receiver=f"{session['email']}", subject="One Time Password for your account registration",body=f"Your OTP for email verification is:{otp1}",file='')

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
                cursor=cnxn.cursor()
                newpassworda=pbkdf2_sha256.hash(form.password.data)
                cursor.execute(f" UPDATE  userinfo  set passwordd = '{newpassworda}' where email='{session['email']}' ")
                cnxn.commit()
                flash('Update successfull', 'success')
                return redirect(url_for('userhome'))
            else:
                flash('Enter Correct old password', 'danger')
                return redirect(url_for('changepass'))

    return render_template('newpass.html',form=form,title="Change Password")

@app.route('/newpass', methods=['GET', 'POST'])
def newpass():
    form=NewPassForm()
    cursor = cnxn.cursor()
    if request.method == 'POST':
        newpassword = form.data['password']
        confirmnewpassword = form.data['cpassword']

        if (newpassword == confirmnewpassword):
            newpassworda = pbkdf2_sha256.hash(newpassword)

            cursor.execute(f" UPDATE  userinfo  set passwordd = '{newpassworda}' where email =  '{session['email']}' ")
            cnxn.commit()
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
    app.run(host='localhost', port=5000, debug=True)
