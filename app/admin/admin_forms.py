from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegenerateImagesForm(FlaskForm):
    dir = StringField('Images directory', validators=[DataRequired()])
    submit1 = SubmitField('Regenerte database')

class DownloadXMLForm(FlaskForm):
    format = SelectField('Format',choices=[('0', 'zip'), ('1', 'CSV')])
    submit2 = SubmitField('Download')

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password')
    mail = StringField('Mail', validators=[DataRequired()])
    send_mail = BooleanField('Send mail to new user')
    submit3 = SubmitField('New User')
