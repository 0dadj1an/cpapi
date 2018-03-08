from flask import render_template
from flask import redirect
from flask import request
from flask import session

from flask_login import UserMixin
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import LoginManager

from app import app
from cap import *

login_manager = LoginManager()
login_manager.init_app(app)

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


@app.before_request
def before_request():
    keepalive_pages = ['custom', 'addhost', 'addnetwork', 'addgroup' 'policy',
                       'showobject', 'commands', 'logout']
    if request.endpoint in keepalive_pages:
        if hasattr(apisession, 'ipaddress'):
            response = apisession.keepalive()
            if response.status_code != 200:
                return redirect('/login')
        else:
            return redirect('/login')


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
        app.logger.info('Login attempt {}@{} > {}'.format(
            username, request.remote_addr, ipaddress))
        response = apisession.login(ipaddress, username, password, domain)
        try:
            if response.status_code != 200:
                try:
                    return render_template(
                        'login.html', feedback=response.json()['message'])
                except Exception as e:
                    app.logger.error('{} - {}'.format(type(e).__name__, e))
                    return render_template(
                        'login.html', feedback=response.text)
        # No connection happened so there is no status code
        except AttributeError as e:
            return render_template('login.html', feedback=response)

        app.logger.info('Login Success {}@{} > {}'.format(
            username, request.remote_addr, ipaddress))
        apisession.sid = response.json()['sid']
        apisession.ipaddress = ipaddress
        user = User(apisession.sid)
        login_user(user)
        misc.pre_data(apisession)
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
        return render_template(
            'custom.html', allcommands=apisession.all_commands)
    if request.method == 'POST':
        command = request.form.get('command')
        payload = request.form.get('payload')
        response = misc.customcommand(apisession, command, payload)
        if command != 'logout':
            try:
                if response.status_code == 403 or response.status_code == 404:
                    return (render_template(
                        'custom.html',
                        allcommands=apisession.all_commands,
                        lastcomm=command,
                        payload=payload,
                        response=str(response)))
                else:
                    return (render_template(
                        'custom.html',
                        allcommands=apisession.all_commands,
                        lastcomm=command,
                        payload=payload,
                        response=response.text))
            except AttributeError:
                response = 'Incorrect payload format.'
                return (render_template(
                    'custom.html',
                    allcommands=apisession.all_commands,
                    lastcomm=command,
                    payload=payload,
                    response=response))
        else:
            return redirect('/login')


@app.route('/addhost', methods=['GET', 'POST'])
@login_required
def addhost():
    if request.method == 'GET':
        return render_template(
            'addhost.html',
            alltargets=apisession.all_targets,
            colors=apisession.all_colors)
    if request.method == 'POST':
        hostdata = request.form.to_dict()
        hostpayload = {
            'name': hostdata['hostname'],
            'ipv4-address': hostdata['hostip'],
            'color': hostdata['hostcolor']
        }
        if 'nat-settings' in hostdata:
            hostpayload.update({
                'nat-settings': {
                    'auto-rule': True,
                    'method': hostdata['method']
                }
            })
            if 'hide-behind' in hostdata:
                hostpayload['nat-settings'].update({
                    'hide-behind':
                    hostdata['hide-behind']
                })
            if 'install-on' in hostdata:
                if hostdata['install-on'] != '':
                    hostpayload['nat-settings'].update({
                        'install-on':
                        hostdata['install-on']
                    })
            if 'natipaddress' in hostdata:
                hostpayload['nat-settings'].update({
                    'ip-address':
                    hostdata['natipaddress']
                })
        response = objects.addhost(apisession, hostpayload)
        if response.status_code == 200:
            apisession.publish()
        return render_template(
            'addhost.html',
            alltargets=apisession.all_targets,
            colors=apisession.all_colors,
            response=response.text)


@app.route('/addnetwork', methods=['GET', 'POST'])
@login_required
def addnetwork():
    if request.method == 'GET':
        return render_template(
            'addnetwork.html',
            alltargets=apisession.all_targets,
            colors=apisession.all_colors)
    if request.method == 'POST':
        netdata = request.form.to_dict()
        netpayload = {
            'name': netdata['netname'],
            'subnet': netdata['network'],
            'subnet-mask': netdata['netmask'],
            'color': netdata['netcolor']
        }
        if 'nat-settings' in netdata:
            netpayload.update({
                'nat-settings': {
                    'auto-rule': True,
                    'method': netdata['method']
                }
            })
            if 'hide-behind' in netdata:
                netpayload['nat-settings'].update({
                    'hide-behind':
                    netdata['hide-behind']
                })
            if 'install-on' in netdata:
                if netdata['install-on'] != '':
                    netpayload['nat-settings'].update({
                        'install-on':
                        netdata['install-on']
                    })
            if 'natipaddress' in netdata:
                netpayload['nat-settings'].update({
                    'ip-address':
                    netdata['natipaddress']
                })
        response = objects.addnetwork(apisession, netpayload)
        if response.status_code == 200:
            apisession.publish()
        return render_template(
            'addnetwork.html',
            alltargets=apisession.all_targets,
            colors=apisession.all_colors,
            response=response.text)


@app.route('/addgroup', methods=['GET', 'POST'])
@login_required
def addgroup():
    if request.method == 'GET':
        return render_template(
            'addgroup.html', colors=apisession.all_colors)
    if request.method == 'POST':
        if 'groupname' in request.form.keys():
            groupname = request.form.get('groupname')
            response = objects.addgroup(apisession, groupname)
        if response.status_code == 200:
            apisession.publish()
        return render_template(
            'addgroup.html',
            colors=apisession.all_colors,
            response=response.text)


@app.route('/policy', methods=['GET', 'POST'])
@login_required
def policy():
    if request.method == 'GET':
        return render_template(
            'policy.html', alllayers=apisession.all_layers)
    if request.method == 'POST':
        layer = request.form.get('layer')
        response = rules.showrulebase(apisession, layer)
        return render_template(
            'policy.html',
            alllayers=apisession.all_layers,
            rulebase=response,
            lastlayer=layer)


@app.route('/showobject/<cp_objectuid>', methods=['GET'])
@login_required
def showobject(cp_objectuid):
    response = objects.show_object(apisession, cp_objectuid)
    return render_template('showobject.html', cpobject=response.json())


@app.route('/commands', methods=['GET', 'POST'])
@login_required
def commands():
    if request.method == 'GET':
        return render_template(
            'commands.html', alltargets=apisession.all_targets)
    if request.method == 'POST':
        if request.form.getlist('target') == [] or request.form.get(
                'command') == '':
            error = 'No target and/or command provided.'
            return render_template(
                'commands.html',
                alltargets=apisession.all_targets,
                error=error)
        targets = request.form.getlist('target')
        command = request.form.get('script')
        response = misc.runcommand(apisession, targets, command)
        return render_template(
            'commands.html',
            alltargets=apisession.all_targets,
            response=response)
