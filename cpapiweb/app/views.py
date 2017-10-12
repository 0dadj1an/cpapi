from flask import render_template, redirect, request, session
from flask_nav import Nav
from flask_nav.elements import Navbar, View

from app import app
from cap import *

nav = Nav()
nav.init_app(app)

def sid_check():
    if 'sid' not in session:
        return(redirect('/login'))

@nav.navigation()
def mynavbar():
    return Navbar(
        'cpapi',
        View('Custom', 'custom'),
        View('Add Object', 'addobject'),
        View('Import Objects', 'importobj'),
        View('Show Rules', 'showrules'),
        View('Run Command', 'runcommand'),
        View('Logout', 'logout'))

@app.errorhandler(500)
def internal_error(e):
    return(render_template('500.html'), 500)

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
        password = request.form.get('password')
        domain = request.form.get('domain', None)

        response = connect.login(session['ipaddress'], session['username'], password, domain)
        try:
            if response.status_code == 200:
                if 'sid' in response.json():
                    session['sid'] = response.json()['sid']
                    session['apiver'] = response.json()['api-server-version']
                    session['allcommands'] = misc.getallcommands(session['ipaddress'], session['sid'])
                    session['alllayers'] = policy.getalllayers(session['ipaddress'], session['sid'])
                    session['alltargets'] = misc.getalltargets(session['ipaddress'], session['sid'])
                    app.logger.info('Login from - ip:{} // user:{} // mgmt:{}'.format(request.remote_addr,
                                                                                      session['username'],
                                                                                      session['ipaddress']))
                    return(redirect('/custom'))
            elif response.status_code == 400:
                return(render_template('login.html', error=response.text))
            else:
                return(render_template('login.html', error=str(response)))
        except AttributeError:
            app.logger.info('Failed login from {}'.format(request.remote_addr))
            return(render_template('login.html', error=str(response)))
        except Exception as e:
            app.logger.error('Unknown exception : {}'.format(e))
            return(render_template('login.html', error=str(response)))

@app.route('/logout', methods=['POST', 'GET'])
def logout():

    if request.method == 'GET':
        sid_check()
        return(render_template('logout.html'))

    if request.method == 'POST':
        sid_check()
        if 'Discard' in request.form:
            utility.logout_session(session, request)
            return(redirect('/login'))
        elif 'Publish' in request.form:
            connect.publish(session['ipaddress'], session['sid'])
            utility.logout_session(session, request)
            return(redirect('/login'))

@app.route('/custom', methods=['POST', 'GET'])
def custom():

    if request.method == 'GET':
        sid_check()
        return(render_template('custom.html', allcommands=session['allcommands']))

    if request.method == 'POST':
        sid_check()
        command = request.form.get('command')
        payload = request.form.get('payload')
        response = misc.customcommand(session['ipaddress'], command, payload, session['sid'])
        if command != 'logout':
            try:
                if response.status_code == 403 or response.status_code == 404:
                    return(render_template('custom.html', allcommands=session['allcommands'], response=str(response)))
                else:
                    return(render_template('custom.html', allcommands=session['allcommands'], response=response.text))
            except Exception as e:
                response = 'Incorrect payload format.'
                return(render_template('custom.html', allcommands=session['allcommands'], response=response))
        else:
            app.logger.info('Logout from - ip:{} // user:{} // mgmt:{}'.format(request.remote_addr,
                                                                              session['username'],
                                                                              session['ipaddress']))
            utility.clear_session(session)
            return(redirect('/login'))

@app.route('/addobject', methods=['POST', 'GET'])
def addobject():

    if request.method == 'GET':
        sid_check()
        session['allhostlist'] = host.getallhosts(session['ipaddress'], session['sid'])
        session['allnetlist'] = network.getallnetworks(session['ipaddress'], session['sid'])
        session['allgrouplist'] = group.getallgroups(session['ipaddress'], session['sid'])
        return(render_template('addobject.html', allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))

    if request.method == 'POST':
        sid_check()
        if 'host' in request.form.keys() or 'network' in request.form.keys() or 'group' in request.form.keys() or 'addgroup' in request.form.keys():
            response = utility.add_object(session, request)
            return(render_template('addobject.html', response=response, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))

@app.route('/importobj', methods=['POST', 'GET'])
def importobj():

    if request.method == 'GET':
        sid_check()
        return(render_template('importobj.html'))

    if request.method == 'POST':
        sid_check()
        checker = utility.import_check(request.files, session)
        if checker['status'] == True:
            return(render_template('importobj.html', report=checker['report']))
        elif checker['status'] == False:
            return (render_template('importobj.html', error=checker['report']))

@app.route('/showrules', methods=['POST', 'GET'])
def showrules():

    if request.method == 'GET':
        sid_check()
        return(render_template('showrules.html', alllayers=session['alllayers']))

    if request.method == 'POST':
        sid_check()
        response = policy.showrulebase(session['ipaddress'], request.form.get('layer'), session['sid'])
        return(render_template('showrules.html', alllayers=session['alllayers'], response=response))

@app.route('/runcommand', methods=['POST', 'GET'])
def runcommand():
    if request.method == 'GET':
        sid_check()
        return(render_template('runcommand.html', alltargets=session['alltargets']))

    if request.method == 'POST':
        sid_check()
        if request.form.getlist('target') == [] or request.form.get('command') == '':
            error = 'No target and/or command provided.'
            return(render_template('runcommand.html', alltargets=session['alltargets'], error=error))
        response = misc.runcommand(session['ipaddress'], request.form.getlist('target'), request.form.get('command'), session['sid'])
        return(render_template('runcommand.html', alltargets=session['alltargets'], response=response))
