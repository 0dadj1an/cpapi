from flask import render_template, redirect, request, session
from app import app
from cap import *

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
            return(redirect('/commands'))
        else:
            return(render_template('login.html', error=response))

@app.route('/commands', methods=['POST', 'GET'])
def commands():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('commands.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        command = request.form.get('command')
        payload = request.form.get('payload')
        response = misc.customcommand(session['ipaddress'], command, payload, session['sid'])
        if command != 'logout':
            return(render_template('commands.html', response=response))
        else:
            session.pop('sid', None)
            return(redirect('/login'))
