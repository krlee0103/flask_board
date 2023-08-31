from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired('required entry.')])
    content = TextAreaField('Content', validators=[DataRequired('required entry.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired('required entry.')])


class UserCreateForm(FlaskForm):
    username = StringField('User id', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', 'Wrong Password')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('User id', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])