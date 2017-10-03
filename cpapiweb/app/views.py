from flask import render_template, redirect, request, session
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from app import app
from cap import *

nav = Nav()
nav.init_app(app)

@nav.navigation()
def mynavbar():
    return Navbar(
        'cpapi',
        View('Custom', 'custom'),
        View('Add Object', 'addobject'),
        View('Show Rules', 'showrules'),
        View('Logout', 'logout'))

@app.route('/')
def index():
    return(redirect('/login'))

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'GET':
        return(render_template('login.html'))

    if request.method == 'POST':
        session['ipaddress'] = request.form.get('ipaddress')
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        session['domain'] = request.form.get('domain', None)

        response = connect.login(session['ipaddress'], session['username'], session['password'], session['domain'])

        try:
            if 'sid' in response.json():
                session['sid'] = response.json()['sid']
                session['apiver'] = response.json()['api-server-version']
                app.logger.info('Successful login from user: {} to mgmt: {}'.format(session['username'], session['ipaddress']))
                return(redirect('/custom'))
        except (ValueError, AttributeError) as e:
            app.logger.info('Caught expected exception on login: {}'.format(e))
            return(render_template('login.html', error=str(response)))
        except Exception as e:
            app.logger.error('Unexpected exception on login: {}'.format(e))
            return(render_template('login.html', error=str(response)))

@app.route('/custom', methods=['POST', 'GET'])
def custom():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('custom.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            command = request.form.get('command')
            payload = request.form.get('payload')
            response = misc.customcommand(session['ipaddress'], command, payload, session['sid'])
            if command != 'logout':
                if response.status_code == 403 or response.status_code == 404:
                    return(render_template('custom.html', response=str(response)))
                else:
                    return(render_template('custom.html', response=response.text))
            else:
                app.logger.info('Successful logout from user: {} to mgmt: {}'.format(session['username'], session['ipaddress']))
                session.pop('sid', None)
                return(redirect('/login'))
        else:
            return(redirect('/login'))

@app.route('/addobject', methods=['POST', 'GET'])
def addobject():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('addobject.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            if 'host' in request.form.keys():
                hostname = request.form.get('hostname')
                ipv4address= request.form.get('ipv4address')
                response = host.addhost(session['ipaddress'], hostname, ipv4address, session['sid'])
                connect.publish(session['ipaddress'], session['sid'])
                try:
                    return(render_template('addobject.html', response=response.text))
                except (ValueError, AttributeError) as e:
                    return(render_template('addobject.html', response=str(response)))
            elif 'network' in request.form.keys():
                netname = request.form.get('netname')
                networkip = request.form.get('network')
                mask = request.form.get('mask')
                response = network.addnetwork(session['ipaddress'], netname, networkip, mask, session['sid'])
                connect.publish(session['ipaddress'], session['sid'])
                try:
                    return(render_template('addobject.html', response=response.text))
                except (ValueError, AttributeError) as e:
                    return(render_template('addobject.html', response=str(response)))
        else:
            return(redirect('/login'))

@app.route('/showrules', methods=['POST', 'GET'])
def showrules():

    if request.method == 'GET':
        if 'sid' in session:
            alllayers = policy.getalllayers(session['ipaddress'], session['sid'])
            return(render_template('showrules.html', alllayers=alllayers))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            alllayers = policy.getalllayers(session['ipaddress'], session['sid'])
            response = policy.showrulebase(session['ipaddress'], request.form.get('layer'), session['sid'])
            return(render_template('showrules.html', alllayers=alllayers, response=response))
        else:
            return(redirect('/login'))

@app.route('/logout', methods=['POST', 'GET'])
def logout():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('logout.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            if 'Discard' in request.form:
                connect.discard(session['ipaddress'], session['sid'])
                connect.logout(session['ipaddress'], session['sid'])
                app.logger.info('Successful logout from user: {} to mgmt: {}'.format(session['username'], session['ipaddress']))
                session.pop('sid', None)
                return(redirect('/login'))
            elif 'Publish' in request.form:
                connect.publish(session['ipaddress'], session['sid'])
                # Discard still required here...because API.
                connect.discard(session['ipaddress'], session['sid'])
                connect.logout(session['ipaddress'], session['sid'])
                app.logger.info('Successful logout from user: {} to mgmt: {}'.format(session['username'], session['ipaddress']))
                session.pop('sid', None)
                return(redirect('/login'))
        else:
            return(redirect('/login'))
