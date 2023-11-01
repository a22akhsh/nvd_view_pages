# This is an analysis of online vulnerability analysis Python Project.
import os
import secrets
import string
from datetime import timedelta


from flask import Flask, request, url_for, render_template, redirect, Response, session
from flask_login import LoginManager, UserMixin, login_manager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import cve_nvd_view


def generate_secret_key(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = generate_secret_key(32)

login_manager = LoginManager()
login_manager.login_view = '/login'  # 'login' should match the route for your login page
login_manager.init_app(app)

# Mock user data (replace with your user model and database)
users = {'root': {'password': 'root'}}


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(username):
    if username in users:
        user = User(username)
        user.id = username
        return user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    form = LoginForm()
    if form.validate_on_submit() or form.is_submitted():
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            user.id = username
            login_user(user)
            return redirect(url_for('cve_nvd_analysis_view'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully'

# Apply the @login_required decorator to the view class
cve_nvd_view.NvdCveView.get = login_required(cve_nvd_view.NvdCveView.get)
# cve_nvd_view.NvdCveView.post = login_required(cve_nvd_view.NvdCveView.post)

if __name__ == '__main__':
    print("execution started")
    # https://localhost:8081/v1/cve/backend/ - Default
    host_address = os.getenv('host_addr', default="https://localhost:8080/v1/cve/nvd_web_front/")
    app.debug = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.add_url_rule("/v1/nvd_view",
                     view_func=cve_nvd_view.NvdCveView.as_view("cve_nvd_analysis_view",
                                                               host_address))
    app.run(host='0.0.0.0', port=8082, ssl_context='adhoc')
