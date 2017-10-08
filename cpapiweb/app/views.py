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
        session['password'] = request.form.get('password')
        session['domain'] = request.form.get('domain', None)

        response = connect.login(session['ipaddress'], session['username'], session['password'], session['domain'])
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
        except Exception as e:
            app.logger.warn('From VIEWS :: {}'.format(e))
            return(render_template('login.html', error=str(response)))

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
                app.logger.info('Logout from - ip:{} // user:{} // mgmt:{}'.format(request.remote_addr,
                                                                                  session['username'],
                                                                                  session['ipaddress']))
                session.pop('sid', None)
                return(redirect('/login'))
            elif 'Publish' in request.form:
                connect.publish(session['ipaddress'], session['sid'])
                # Discard still required here...because API.
                connect.discard(session['ipaddress'], session['sid'])
                connect.logout(session['ipaddress'], session['sid'])
                app.logger.info('Logout from - ip:{} // user:{} // mgmt:{}'.format(request.remote_addr,
                                                                                  session['username'],
                                                                                  session['ipaddress']))
                utility.clear_session(session)
                return(redirect('/login'))
        else:
            return(redirect('/login'))

@app.route('/custom', methods=['POST', 'GET'])
def custom():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('custom.html', allcommands=session['allcommands']))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
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
                    app.logger.error('From VIEWS :: {}'.format(e))
                    response = 'Incorrect payload format.'
                    return(render_template('custom.html', allcommands=session['allcommands'], response=response))
            else:
                app.logger.info('Logout from - ip:{} // user:{} // mgmt:{}'.format(request.remote_addr,
                                                                                  session['username'],
                                                                                  session['ipaddress']))
                session.pop('sid', None)
                return(redirect('/login'))
        else:
            return(redirect('/login'))

@app.route('/addobject', methods=['POST', 'GET'])
def addobject():

    if request.method == 'GET':
        if 'sid' in session:
            session['allhostlist'] = host.getallhosts(session['ipaddress'], session['sid'])
            session['allnetlist'] = network.getallnetworks(session['ipaddress'], session['sid'])
            session['allgrouplist'] = group.getallgroups(session['ipaddress'], session['sid'])
            return(render_template('addobject.html', allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            if 'host' in request.form.keys() or 'network' in request.form.keys() or 'group' in request.form.keys() or 'addgroup' in request.form.keys():
                response = utility.add_object(session, request)
                return(render_template('addobject.html', response=response, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
            else:
                print('nope')
        else:
            return(redirect('/login'))

@app.route('/importobj', methods=['POST', 'GET'])
def importobj():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('importobj.html'))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            checker = utility.import_object(request.files, session)
            if checker['status'] == True:
                return(render_template('importobj.html', report=checker['report']))
            elif checker['status'] == False:
                return (render_template('importobj.html', error=checker['report']))
        else:
            return(redirect('/login'))

@app.route('/showrules', methods=['POST', 'GET'])
def showrules():

    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('showrules.html', alllayers=session['alllayers']))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            response = policy.showrulebase(session['ipaddress'], request.form.get('layer'), session['sid'])
            return(render_template('showrules.html', alllayers=session['alllayers'], response=response))
        else:
            return(redirect('/login'))

@app.route('/runcommand', methods=['POST', 'GET'])
def runcommand():
    if request.method == 'GET':
        if 'sid' in session:
            return(render_template('runcommand.html', alltargets=session['alltargets']))
        else:
            return(redirect('/login'))

    if request.method == 'POST':
        if 'sid' in session:
            print(request.form.getlist('target'))
            if request.form.getlist('target') == [] or request.form.get('command') == '':
                error = 'No target and/or command provided.'
                return(render_template('runcommand.html', alltargets=session['alltargets'], error=error))
            response = misc.runcommand(session['ipaddress'], request.form.getlist('target'), request.form.get('command'), session['sid'])
            return(render_template('runcommand.html', alltargets=session['alltargets'], response=response))
        else:
            return(redirect('/login'))
