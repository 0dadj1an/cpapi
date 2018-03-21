from flask import jsonify
from flask import render_template
from flask import redirect
from flask import request
from flask_login import UserMixin
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import LoginManager
from flask_restful import Resource
from flask_restful import Api

from app import app
from app.checkpoint import CheckPoint

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

apisession = None


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.errorhandler(401)
def page_not_found(e):
    return redirect('/login')


@app.errorhandler(500)
def internal_error(e):
    pass


@app.before_request
def before_request():
    pass


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
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
            apisession.verify_db()
            user = User(apisession.sid)
            login_user(user)
            return redirect('/sandbox')
        else:
            app.logger.info('Login failure {}@{} > {}'.format(
                loginform['user'], request.remote_addr, loginform['ipaddress']))
            app.logger.info(response)
            return render_template('login.html', feedback=response)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if request.method == 'GET':
        apisession.dbobj.cursor.close()
        apisession.dbobj.dbconn.close()
        apisession.logout()
        logout_user()
        return redirect('/login')


@app.route('/sandbox', methods=['GET', 'POST'])
@login_required
def sandbox():
    if request.method == 'GET':
        return render_template(
            'sandbox.html', allcommands=apisession.all_commands)
    elif request.method == 'POST':
        json = request.get_json()
        response = apisession.customcommand(json['command'], json['payload'])
        return jsonify(response)


@app.route('/objects', methods=['GET', 'POST'])
@login_required
def objects():
    if request.method == 'GET':
        object_status = apisession.object_status()
        return render_template('objects.html', objectstatus=object_status)


@app.route('/policy', methods=['GET', 'POST'])
@login_required
def policy():
    if request.method == 'GET':
        return render_template('policy.html', alllayers=apisession.all_layers, allobjects='')


@app.route('/showobject/<cp_objectuid>', methods=['GET'])
@login_required
def showobject(cp_objectuid):
    app.logger.info('Displaying Check Point Object {}.'.format(cp_objectuid))
    response = apisession.show_object(cp_objectuid)
    return render_template('showobject.html', cpobject=response.json())


@app.route('/scripts', methods=['GET', 'POST'])
@login_required
def scripts():
    if request.method == 'GET':
        return render_template(
            'scripts.html', alltargets=apisession.all_targets)
    elif request.method == 'POST':
        if request.form.getlist('targets') == [] or request.form.get(
                'script') == '':
            error = 'No target and/or command provided.'
            return render_template(
                'scripts.html',
                alltargets=apisession.all_targets,
                error=error)
        else:
            targets = request.form.getlist('targets')
            command = request.form.get('script')
            app.logger.info('Running script "{}"'.format(command))
            response = apisession.runcommand(targets, command)
            return render_template(
                'scripts.html',
                alltargets=apisession.all_targets,
                response=response)


class ObjectCheck(Resource):
    def get(self):
        if apisession.sid:
            object_status = apisession.object_status()
            return jsonify(object_status)


class FullSync(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            apisession.full_sync()


class DeltaSync(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            apisession.delta_sync()


class ShowHosts(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            response = apisession.dbobj.get_hosts()
            return jsonify(response)


class ShowNetworks(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            response = apisession.dbobj.get_networks()
            return jsonify(response)


class ShowGroups(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            response = apisession.dbobj.get_groups()
            return jsonify(response)


class ShowAccessRoles(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            response = apisession.dbobj.get_access_roles()
            return jsonify(response)


class ShowServers(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            response = apisession.dbobj.get_servers()
            return jsonify(response)


class ShowServices(Resource):
    def get(self):
        if hasattr(apisession, 'sid'):
            response = apisession.dbobj.get_services()
            return jsonify(response)


class ShowRules(Resource):
    def post(self):
        if hasattr(apisession, 'sid'):
            data = request.get_json()
            response = apisession.show_rules(**data)
            return jsonify(response)


class AddRule(Resource):
    def put(self):
        if hasattr(apisession, 'sid'):
            data = request.get_json()
            response = apisession.add('access-rule', **data)
            return jsonify(response)


class EditRule(Resource):
    def post(self):
        if hasattr(apisession, 'sid'):
            data = request.get_json()
            response = apisession.set('access-rule', **data)
            return jsonify(response)


class DeleteRule(Resource):
    def delete(self):
        if hasattr(apisession, 'sid'):
            data = request.get_json()
            response = apisession.delete('access-rule', **data)
            return jsonify(response)


api.add_resource(ObjectCheck, '/objects/objectcheck')
api.add_resource(FullSync, '/objects/fullsync')
api.add_resource(DeltaSync, '/objects/deltasync')
api.add_resource(ShowHosts, '/objects/showhosts')
api.add_resource(ShowNetworks, '/objects/shownetworks')
api.add_resource(ShowGroups, '/objects/showgroups')
api.add_resource(ShowAccessRoles, '/objects/showaccessroles')
api.add_resource(ShowServers, '/objects/showservers')
api.add_resource(ShowServices, '/objects/showservices')
api.add_resource(ShowRules, '/policy/showrules')
api.add_resource(AddRule, '/policy/addrule')
api.add_resource(EditRule, '/policy/editrule')
api.add_resource(DeleteRule, '/policy/deleterule')
