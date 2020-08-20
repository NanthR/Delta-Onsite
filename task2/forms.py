from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField

class RequestReset(Form):
	email = StringField('Email', [validators.DataRequired(), validators.Email()])
	submit = SubmitField('Reset')

class ChangePassword(Form):
	password = PasswordField('Password', [validators.DataRequired()])
	confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])
	submit = SubmitField('Submit')

class Login(Form):
	username = StringField('User Name', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Submit')