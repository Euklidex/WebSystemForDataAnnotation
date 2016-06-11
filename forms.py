from wtforms import Form, StringField, SubmitField, validators


class UserLoginForm(Form):
    name = StringField('Name', [validators.required()])
    password = StringField('Password', [validators.required()])
    submit = SubmitField('Login')
