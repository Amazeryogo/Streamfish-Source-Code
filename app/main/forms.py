from flask import request
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    email = StringField(_l('Email'),validators=[DataRequired()])
    darkmode = BooleanField(_l('Dark Mode?'))
    hindi = BooleanField(_l('Hindi? (Beta)'))
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Post it'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Send A message'), validators=[
        DataRequired(), Length(min=1, max=10000000)])
    submit = SubmitField(_l('Send'))


class EditProfileFormHINDI(FlaskForm):
    username = StringField(_l('उपयोगकर्ता नाम'), validators=[DataRequired()])
    about_me = TextAreaField(_l('मेरे बारे मेँ'),
                             validators=[Length(min=0, max=140)])
    email = StringField(_l('ईमेल'),validators=[DataRequired()])
    darkmode = BooleanField(_l('डार्क मोड?'))
    hindi = BooleanField(_l('हिंदी (बीटा)'))
    submit = SubmitField(_l('प्रस्तुत'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileFormHINDI, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('कृपया एक अलग उपयोगकर्ता नाम का उपयोग करें।'))


class EmptyFormHINDI(FlaskForm):
    submit = SubmitField('प्रस्तुत')


class PostFormHINDI(FlaskForm):
    post = TextAreaField(_l('बोलो भी'), validators=[DataRequired()])
    submit = SubmitField(_l('इसे पोस्ट करें'))


class SearchFormHINDI(FlaskForm):
    q = StringField(_l('जाँच'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchFormHINDI, self).__init__(*args, **kwargs)


class MessageFormHINDI(FlaskForm):
    message = TextAreaField(_l('संदेश'), validators=[
        DataRequired(), Length(min=1, max=10000000)])
    submit = SubmitField(_l('भेज देना'))


class Longboy(FlaskForm):
    title = StringField(_l('Title'),validators=[
        DataRequired(), Length(min=5, max=200)])
    body = TextAreaField(_l('Body'),validators=[
        DataRequired(), Length(min=5, max=5000)])
    submit = SubmitField(_l('Post it!'))    