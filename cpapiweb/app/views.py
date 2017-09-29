from flask import render_template, redirect, request
from app import app
from cap import *

class Connection:

    def __init__(self, ipaddress, sid, apiver):
        self.ipaddress = ipaddress
        self.sid = sid
        self.apiver = apiver

    def update(self, ipaddress, sid, apiver):
        self.ipaddress = ipaddress
        self.sid = sid
        self.apiver = apiver

conn1 = Connection('tbd', 'tbd', 'tbd')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'GET':
        return(render_template('login.html'))

    if request.method == 'POST':
        ipaddress = request.form.get('ipaddress')
        username = request.form.get('username')
        password = request.form.get('password')
        domain = request.form.get('domain', None)

        response = session.login(ipaddress, username, password, domain)
        if 'sid' in response:
            conn1.update(ipaddress, response['sid'], response['api-server-version'])
            return(redirect('/commands'))
        else:
            return(render_template('login.html', error=response))

@app.route('/commands', methods=['POST', 'GET'])
def commands():

    if request.method == 'GET':
        return(render_template('commands.html'))

    if request.method == 'POST':
        command = request.form.get('command')
        payload = request.form.get('payload')
        response = misc.customcommand(conn1.ipaddress, command, payload, conn1.sid)
        if command != 'logout':
            return(render_template('commands.html', response=response))
        else:
            return(redirect('/login'))
