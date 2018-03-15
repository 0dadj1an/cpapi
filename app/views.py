from flask import jsonify
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
        response = apisession.login()
        if apisession.sid:
            app.logger.info('Login success {}@{} > {}'.format(
                loginform['user'], request.remote_addr, loginform['ipaddress']))
            apisession.pre_data()
            user = User(apisession.sid)
            login_user(user)
            return redirect('/custom')
        else:
            app.logger.info('Login failure {}@{} > {}'.format(
                loginform['user'], request.remote_addr, loginform['ipaddress']))
            app.logger.info(response)
            return render_template('login.html', feedback=response)


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
        json = request.get_json()
        response = apisession.customcommand(json['command'], json['payload'])
        return jsonify(response)


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
        json = request.get_json()
        app.logger.info('Running script "{}"'.format(json['command']))
        response = apisession.runcommand(json['targets'], json['command'])
        return render_template(
            'commands.html',
            alltargets=apisession.all_targets,
            response=response)
