from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, HiddenField,validators,EmailField,Form
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from wtforms.widgets import TextArea


class SignupForm(FlaskForm):
    first_name=StringField('First Name',validators=[DataRequired()])
    last_name=StringField('Last Name',validators=[DataRequired()])
    email=EmailField('Email',validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password',validators=[DataRequired()])
    submit=SubmitField('Sign up')


class PostForm(FlaskForm):
    title=StringField('Title' ,validators=[DataRequired()])
    contentpost=CKEditorField('Content',validators=[DataRequired()],widget=TextArea())
    lessonname = HiddenField()
    submit=SubmitField('Create Thread')

class PostReply(FlaskForm):
    content=CKEditorField('Content',validators=[DataRequired()],widget=TextArea())
    blog_id = HiddenField()
    submit=SubmitField('Post Reply')