from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# Made with help from Copilot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkeydonttellanyone'
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Ensure template auto-reloading for development
app.template_folder = 'templates'  # Set the template folder

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Your form definition
class EmailForm(FlaskForm):
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name_form = NameForm()
    email_form = EmailForm()

    name = session.get('name')  # Retrieve name from session
    email = session.get('email')  # Retrieve email from session

    if name_form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != name_form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = name_form.name.data


    if email_form.validate_on_submit():
        old_email = session.get('email')
        if old_email is not None and old_email != email_form.email.data:
            flash('Looks like you have changed your email!')
        session['email'] = email_form.email.data

    return render_template('index.html', name=name, email=email, name_form=name_form, email_form=email_form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
                           name=name,
                           current_time=datetime.utcnow())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
