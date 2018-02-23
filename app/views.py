from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session

from flask_nav import Nav
from flask_nav.elements import Navbar
from flask_nav.elements import View

from flask_login import UserMixin
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import LoginManager

from app import app
from cap import *

login_manager = LoginManager()
login_manager.init_app(app)
nav = Nav()
nav.init_app(app)

apisession = connect.APISession()

class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.errorhandler(401)
def page_not_found(e):
    return redirect('/login')


@nav.navigation()
def mynavbar():
    return Navbar('cpapi',
                  View('Login', 'login'),
                  View('Custom', 'custom'),
                  View('Logout', 'logout'))


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        ipaddress = request.form.get('ipaddress')
        username = request.form.get('username')
        password = request.form.get('password')
        domain = request.form.get('domain', None)

        response = apisession.login(ipaddress, username, password, domain)

        if response:
            return render_template('login.html', feedback=response)

        user = User(apisession.sid)
        login_user(user)

        return redirect('/custom')


@app.route('/logout', methods=['GET'])
@login_required
def logout():

    if request.method == 'GET':
        apisession.logout()
        logout_user()
        return redirect('/login')


@app.route('/custom', methods=['GET', 'POST'])
@login_required
def custom():

    if request.method == 'GET':
        allcommands = misc.getallcommands(apisession.ipaddress, apisession.sid)
        return render_template('custom.html', allcommands=allcommands)

    if request.method == 'POST':
        allcommands = misc.getallcommands(apisession.ipaddress, apisession.sid)
        command = request.form.get('command')
        payload = request.form.get('payload')

        response = misc.customcommand(apisession.ipaddress, command, payload, apisession.sid)
        if command != 'logout':
            try:
                if response.status_code == 403 or response.status_code == 404:
                    return(render_template('custom.html', allcommands=allcommands, response=str(response)))
                else:
                    return(render_template('custom.html', allcommands=allcommands, response=response.text))
            except Exception as e:
                response = 'Incorrect payload format.'
                return(render_template('custom.html', allcommands=allcommands, response=response))
        else:
            utility.clear_session(session)
            return redirect('/login')
