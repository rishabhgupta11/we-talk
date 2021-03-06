from flask_wtf import Form
from models import User
from wtforms import StringField, PasswordField, TextAreaField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User already exists")


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User already exists")


class RegisterForm(Form):
    name = StringField(
        'Name',
        validators=[
            DataRequired()
        ]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers and underscores only")

            ),
            name_exists
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords do not match')
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ]
    )


class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )


class PostForm(Form):
    content = TextAreaField(
        "What's happening?",
        validators=[
            DataRequired()
        ]
    )
    image = FileField(
        'Image',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only!')
        ],
        default=None
    )

#comment field on post
class CommentForm(Form):
    comment = TextAreaField(
        "Add a Comment",
        validators=[
            DataRequired()
        ]
    )
