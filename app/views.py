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
from app.checkpoint import CheckPoint

login_manager = LoginManager()
login_manager.init_app(app)

apisession = ''

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
    keepalive_pages = [
        'custom', 'addhost', 'addnetwork', 'addgroup'
        'policy', 'showobject', 'commands', 'logout'
    ]
    if request.endpoint in keepalive_pages:
        if apisession.sid:
            response = apisession.keepalive()
            if response['message'] != 'OK':
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
        global apisession
        loginform = request.form.to_dict()
        app.logger.info('Login attempt {}@{} > {}'.format(
            loginform['user'], request.remote_addr, loginform['ipaddress']))
        apisession = CheckPoint(loginform['ipaddress'], loginform['user'],
            password=loginform['password'], domain=loginform['domain'])
        apisession.login()
        if apisession.sid:
            apisession.pre_data()
            user = User(apisession.sid)
            login_user(user)
            return redirect('/custom')
        else:
            print('failed login')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if request.method == 'GET':
        apisession.logout()
        logout_user()
        return redirect('/login')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        apisession.verify_obj()
        return render_template(
            'settings.html',
            remote=apisession.remote_obj,
            local=apisession.local_obj)
    if request.method == 'POST':
        apisession.verify_obj()
        if apisession.local_obj != 0:
            if apisession.local_obj != apisession.remote_obj:
                if apisession.local_obj > apisession.remote_obj:
                    app.logger.info(
                        'Deleting local objects that are inconsistent.')
                    apisession.deldifobjects()
                    apisession.getdifobjects()
                else:
                    app.logger.info(
                        'Retreiving remote objects that are inconsistent.')
                    apisession.getdifobjects()
            else:
                # Use js in future to disable button if objects are equal.
                app.logger.warn('Equal Retrieve attempted.')
                pass
        else:
            app.logger.info('Initial retrieve of objects.')
            apisession.getallobjects()
        apisession.verify_obj()
        return render_template(
            'settings.html',
            remote=apisession.remote_obj,
            local=apisession.local_obj)


@app.route('/custom', methods=['GET', 'POST'])
@login_required
def custom():
    if request.method == 'GET':
        return render_template(
            'custom.html', allcommands=apisession.all_commands)
    if request.method == 'POST':
        print(request.__dict__)
        print(request.get_json())
        response = apisession.customcommand(command, payload)
        if command != 'logout':
            return jsonify(response)
        else:
            return redirect('/logout')


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
        app.logger.info('Adding Check Point Host.')
        response = apisession.addhost(hostpayload)
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
        app.logger.info('Adding Check Point Network.')
        response = apisession.addnetwork(netpayload)
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
        all_objects = apisession.get_local_objs()
        return render_template(
            'addgroup.html',
            colors=apisession.all_colors,
            allobjects=all_objects)
    if request.method == 'POST':
        app.logger.info('Adding Check Point Group.')
        all_objects = apisession.get_local_objs()
        if 'groupname' in request.form.keys():
            groupname = request.form.get('groupname')
            groupcolor = request.form.get('groupcolor')
            members = request.form.getlist('members')
            response = apisession.addgroup(groupname, groupcolor, members)
        if response.status_code == 200:
            apisession.publish()
        return render_template(
            'addgroup.html',
            colors=apisession.all_colors,
            allobjects=all_objects,
            response=response.text)


@app.route('/policy', methods=['GET', 'POST'])
@login_required
def policy():
    if request.method == 'GET':
        return render_template('policy.html', alllayers=apisession.all_layers)
    if request.method == 'POST':
        app.logger.info('Retrieving local objects for policy view.')
        all_objects = apisession.get_local_objs()
        formdata = request.form.to_dict()
        if 'delete' in formdata:
            rulenum = formdata['delete']
            app.logger.info('Deleting rule number {} from {}'.format(
                rulenum, apisession.lastlayer))
            feedback = apisession.delete_rule(rulenum)
        if 'add' in formdata:
            ruledata = {
                'position': request.form.get('position'),
                'name': request.form.get('name'),
                'source': request.form.getlist('source'),
                'destination': request.form.getlist('destination'),
                'service': request.form.getlist('service'),
                'action': request.form.get('action'),
                'track': {
                    'type': request.form.get('track')
                },
                'layer': apisession.lastlayer,
                'install-on': request.form.getlist('install-on')
            }
            app.logger.info('Adding rule number {} to {}'.format(
                ruledata['position'], ruledata['layer']))
            feedback = apisession.add_rule(ruledata)
        if 'layer' in formdata:
            apisession.lastlayer = formdata['layer']
            response = apisession.showrulebase(formdata['layer'])
            return render_template(
                'policy.html',
                alllayers=apisession.all_layers,
                rulebase=response,
                lastlayer=apisession.lastlayer,
                allobjects=all_objects)
        else:
            app.logger.info('Retrieving rulebase after modification.')
            response = apisession.showrulebase(apisession.lastlayer)
            return render_template(
                'policy.html',
                alllayers=apisession.all_layers,
                rulebase=response,
                lastlayer=apisession.lastlayer,
                allobjects=all_objects,
                feedback=feedback)


@app.route('/showobject/<cp_objectuid>', methods=['GET'])
@login_required
def showobject(cp_objectuid):
    app.logger.info('Displaying Check Point Object {}.'.format(cp_objectuid))
    response = apisession.show_object(cp_objectuid)
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
        app.logger.info('Running script "{}"'.format(command))
        response = apisession.runcommand(targets, command)
        return render_template(
            'commands.html',
            alltargets=apisession.all_targets,
            response=response)
