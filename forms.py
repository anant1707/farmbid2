from flask_wtf import FlaskForm as Form
from wtforms import StringField,TextAreaField,PasswordField,SelectField,SubmitField,IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email,EqualTo
from flask_wtf.file import FileField,FileAllowed

class RegistrationForm(Form):
   first_name = StringField("First Name",validators=[InputRequired(),Length(min=2,max=30)])
   last_name= StringField("Last Name",validators=[InputRequired(),Length(min=2,max=30)])
   phone=StringField("Phone Number",validators=[InputRequired(),Length(max=10,min=10)])
   email=StringField('Email',validators=[InputRequired(),Email()])
   password=PasswordField("Password",validators=[InputRequired(),Length(min=8,max=20)])
   cpassword = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=8, max=20),EqualTo('password')])
   submit=SubmitField("Sign Up")

class fileform(Form):
   submit=SubmitField("Submit")

class LoginForm(Form):
   email = StringField('Email', validators=[InputRequired(), Email()])
   password=PasswordField("Password",validators=[InputRequired(),Length(min=8,max=20)])
   submit=SubmitField("Login")
class EmptyForm(Form):
   a=6

class ForgotForm(Form):
   phone = StringField("Enter Registered Phone Number", validators=[InputRequired()])
   submit = SubmitField("Request Otp")


class ResetForm(Form):
   otp = StringField("ENTER OTP", validators=[InputRequired()])
   submit = SubmitField("SUBMIT")

class NewPassForm(Form):
   password = PasswordField("Enter New Password", validators=[InputRequired(), Length(min=8, max=20)])
   cpassword = PasswordField("Confirm Password",validators=[InputRequired(), Length(min=8, max=20), EqualTo('password')])
   submit = SubmitField("UPDATE")

class ChangePassword(NewPassForm):
   oldpassword= PasswordField("Enter Existing Password", validators=[InputRequired(), Length(min=8, max=20)])
   password = PasswordField("Enter New Password", validators=[InputRequired(), Length(min=8, max=20)])
   cpassword = PasswordField("Confirm Password",validators=[InputRequired(), Length(min=8, max=20), EqualTo('password')])
   submit = SubmitField("UPDATE")

