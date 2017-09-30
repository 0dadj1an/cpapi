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
        View('Add Host', 'addhost'),
        View('Add Network', 'addnetwork'))

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

        if 'sid' in response:
            session['sid'] = response['sid']
            session['apiver'] = response['api-server-version']
            return(redirect('/custom'))
        else:
            response = str(response)
            return(render_template('login.html', error=response))

@app.route('/custom', methods=['POST', 'GET'])
def custom():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('custom.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        command = request.form.get('command')
        payload = request.form.get('payload')
        response = misc.customcommand(session['ipaddress'], command, payload, session['sid'])
        if command != 'logout':
            return(render_template('custom.html', response=response))
        else:
            session.pop('sid', None)
            return(redirect('/login'))

@app.route('/addhost', methods=['POST', 'GET'])
def addhost():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('addhost.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        hostname = request.form.get('hostname')
        command = 'add-host'
        ipv4address= request.form.get('ipv4address')
        payload = {'name':hostname, 'ipv4-address':ipv4address}
        response = misc.customcommand(session['ipaddress'], command, str(payload), session['sid'])
        misc.customcommand(session['ipaddress'], 'publish', '{}', session['sid'])
        return(render_template('addhost.html', response=response))

@app.route('/addnetwork', methods=['POST', 'GET'])
def addnetwork():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('addnetwork.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        netname = request.form.get('netname')
        network = request.form.get('network')
        mask = request.form.get('mask')
        command = 'add-network'
        payload = {'name':netname, 'subnet':network, 'subnet-mask':mask}
        response = misc.customcommand(session['ipaddress'], command, str(payload), session['sid'])
        misc.customcommand(session['ipaddress'], 'publish', '{}', session['sid'])
        return(render_template('addnetwork.html', response=response))
