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

        loginapi = session.login(ipaddress, username, password, domain)
        if loginapi == 'error':
            return(render_template('login.html', error='Some error occurred, check connectivity and credentials.'))
        elif loginapi:
            conn1.update(ipaddress, loginapi['sid'], loginapi['api-server-version'])
            return(redirect('/commands'))

@app.route('/commands', methods=['POST', 'GET'])
def commands():

    if request.method == 'GET':
        return(render_template('commands.html'))

    if request.method == 'POST':
        command = request.form.get('command')
        payload = request.form.get('payload')
        response = misc.customcommand(conn1.ipaddress, command, payload, conn1.sid)
        return(render_template('commands.html', response=response))
