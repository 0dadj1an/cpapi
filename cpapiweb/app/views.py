from flask import render_template, redirect, request, session
from werkzeug import secure_filename
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import os, itertools

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
                return(render_template('login.html', error=response.json()))
            else:
                return(render_template('login.html', error=str(response)))
        except:
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
            if 'host' in request.form.keys():
                hostname = request.form.get('hostname')
                ipv4address= request.form.get('ipv4address')
                response = host.addhost(session['ipaddress'], hostname, ipv4address, session['sid'])
                try:
                    return(render_template('addobject.html', response=response.text, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                except (ValueError, AttributeError) as e:
                    return(render_template('addobject.html', response=str(response), allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                except Exception as e:
                    app.logger.error('FROM VIEWS - Unknown exception - {}'.format(e))
                    return(render_template('addobject.html', response='oops', allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
            elif 'network' in request.form.keys():
                netname = request.form.get('netname')
                networkip = request.form.get('network')
                mask = request.form.get('mask')
                response = network.addnetwork(session['ipaddress'], netname, networkip, mask, session['sid'])
                try:
                    return(render_template('addobject.html', response=response.text, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                except (ValueError, AttributeError) as e:
                    return(render_template('addobject.html', response=str(response), allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                except Exception as e:
                    app.logger.error('FROM VIEWS - Unknown exception - {}'.format(e))
                    return(render_template('addobject.html', response='oops', allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
            elif 'group' in request.form.keys():
                groupname = request.form.get('groupname')
                response = group.addgroup(session['ipaddress'], groupname, session['sid'])
                try:
                    return(render_template('addobject.html', response=response.text, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                except (ValueError, AttributeError) as e:
                    return(render_template('addobject.html', response=str(response), allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                except Exception as e:
                    app.logger.error('FROM VIEWS - Unknown exception - {}'.format(e))
                    return(render_template('addobject.html', response='oops', allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
            elif 'addgroup' in request.form.keys():
                hostselection = request.form.getlist('hosts')
                netsselection = request.form.getlist('networks')
                grpsselection = request.form.getlist('groups')
                if hostselection or netsselection or grpsselection:
                    members = []
                    for hst, net, grp in itertools.zip_longest(hostselection, netsselection, grpsselection):
                        members.append(hst)
                        members.append(net)
                        members.append(grp)
                    # I
                    for item in members:
                        if item == None:
                            members.remove(item)
                    # DONT
                    for item in members:
                        if item == None:
                            members.remove(item)
                    # KNOW
                    for item in members:
                        if item == None:
                            members.remove(item)
                    trggselection = request.form.get('trggroup')
                    response = group.setgroup(session['ipaddress'], trggselection, members, session['sid'])
                    return(render_template('addobject.html', response=response.text, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
                else:
                    error = 'Please select some group members.'
                    return(render_template('addobject.html', error=error, allhostlist=session['allhostlist'], allnetlist=session['allnetlist'], allgrouplist=session['allgrouplist']))
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
            checker = utility.import_check(request.files, session)
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
