from flask import render_template
from flask import redirect
from app import app
from flask import request
from cpapipackage import *

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
    if request.method == 'POST':
        ipaddress = request.form.get('ipaddress')
        username = request.form.get('username')
        password = request.form.get('password')
        domain = request.form.get('domain', None)

        loginapi = session.login(ipaddress, username, password, domain)
        if loginapi['sid']:
            conn1.update(ipaddress, loginapi['sid'], loginapi['apiver'])
            return(redirect('/commands'))

    if request.method == 'GET':
        return(render_template('login.html'))

@app.route('/commands', methods=['POST', 'GET'])
def commands():
    if request.method == 'POST':
        command = request.form.get('command')
        payload = request.form.get('payload')
        sendcommand = misc.customcommand(conn1.ipaddress, command, payload, conn1.sid)
        return(render_template('commands.html'))

    if request.method == 'GET':
        return(render_template('commands.html'))
