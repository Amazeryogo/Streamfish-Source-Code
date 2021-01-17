from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('My Username'), validators=[DataRequired()])
    password = PasswordField(_l('My Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Please remember me!'))
    submit = SubmitField(_l('Let\'s go back!'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('My New Username'), validators=[DataRequired()])
    email = StringField(_l('My Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('My New Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat my new Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Lets Go!!'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Hmmm! Try a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Hmmm! Try a different email address'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Reset it Please'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Change my password'))
