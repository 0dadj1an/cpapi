import ast
import base64
import json
import os
import requests
import time

from app import app
from app import localdb

from cpapilib.cpapilib.api import Management_API

class CheckPoint_API(Management_API):
    def __init__(self):
        self.limit = 50
        self.offset = 0
        self.ipaddress = None
        self.domain = None
        self.sid = None
        self.port = '443'
        self.local_obj = 0
        self.remote_obj = 0
        # Consider single/plural dict of these to eliminate service hacking.
        self.obj_map = {
            'host': 'hosts',
            'network': 'networks',
            'group': 'groups',
            'simple-gateway': 'gateways-and-servers',
            'access-role': 'access-roles',
            'service-tcp': 'services-tcp',
            'service-udp': 'services-udp',
            'service-group': 'service-groups'
        }
        self.request_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CPAPI v{}'.format(app.config['version'])
        }
        # Permanently Disable verify for now.
        requests.packages.urllib3.disable_warnings()

    @staticmethod
    def base64_ascii(base64resp):
        """Converts base64 to ascii for run command/showtask."""
        return base64.b64decode(base64resp).decode('utf-8')

    @property
    def url(self):
        """Standard URL for all Management API Calls."""
        return 'https://{}:{}/web_api/'.format(self.ipaddress, self.port)

    def verify_db(self):
        if self.domain:
            self.localdb = '{}{}_{}.db'.format(app.config['BASEDIR'],
                                               self.ipaddress, self.domain)
        else:
            self.localdb = '{}{}.db'.format(app.config['BASEDIR'],
                                            self.ipaddress)
        if not os.path.exists(self.localdb):
            app.logger.info('Creating local DB {}'.format(self.localdb))
            localdb.createdb(self.localdb)
        self.dbobj = localdb.cplocaldb(self.localdb)

    def verify_obj(self):
        self.countallobjects()
        self.local_obj = self.dbobj.object_counter()

    def api_call(self, command, json_payload):
        if self.sid:
            self.request_headers.update({'X-chkp-sid': self.sid})
        try:
            app.logger.info('Command Issued: {}'.format(command))
            response = requests.post(
                self.url + command,
                data=json.dumps(json_payload),
                headers=self.request_headers,
                timeout=(15, 300),
                verify=False)
            return response
        except requests.exceptions.RequestException as e:
            app.logger.error('{}'.format(e))
            return 'Error: {}'.format(e)

    def login(self, ipaddress, username, password, domain=None):
        """Login to Check Point API."""
        self.ipaddress = ipaddress
        payload = {
            'user': username,
            'password': password,
        }
        self.domain = domain
        if domain:
            payload.update({'domain': domain})
        response = self.api_call('login', payload)
        if response.status_code == 200:
            self.verify_db()
        return response

    def publish(self):
        """Publish changes to Check Point."""
        response = self.api_call('publish', {})
        return response

    def discard(self):
        """Discard changes to Check Point."""
        response = self.api_call('discard', {})
        return response

    def keepalive(self):
        """Keepalive Check Point session."""
        response = self.api_call('keepalive', {})
        return response

    def logout(self):
        """Logout of Check Point."""
        response = self.api_call('logout', {})
        return response

    def pre_data(self):
        """Data to establish after login to make less calls later to the API."""
        # Black omitted as defalut option.
        self.all_colors = [
            'aquamarine', 'blue', 'crete blue', 'burlywood', 'cyan',
            'dark green', 'khaki', 'orchid', 'dark orange', 'dark sea green',
            'pink', 'turquoise', 'dark blue', 'firebrick', 'brown',
            'forest green', 'gold', 'dark gold', 'gray', 'dark gray',
            'light green', 'lemon chiffon', 'coral', 'sea green', 'sky blue',
            'magenta', 'purple', 'slate blue', 'violet red', 'navy blue',
            'olive', 'orange', 'red', 'sienna', 'yellow'
        ]
        self.all_commands = self.getallcommands()
        self.all_targets = self.getalltargets()
        self.all_layers = self.getalllayers()

    def addhost(self, hostpayload):
        add_host_response = self.api_call('add-host', hostpayload)
        return add_host_response

    def addnetwork(self, netpayload):
        add_net_response = self.api_call('add-network', netpayload)
        return add_net_response

    def addgroup(self, groupname, color, members):
        add_group_data = {
            'name': groupname,
            'color': color,
            'members': members
        }
        add_group_response = self.api_call('add-group', add_group_data)
        return add_group_response

    def show_object(self, objuid):
        show_obj_data = {'uid': objuid}
        show_obj_response = self.api_call('show-object', show_obj_data)
        type_obj_data = {'uid': objuid, 'details-level': 'full'}
        type_obj_response = self.api_call('show-{}'.format(
            show_obj_response.json()['object']['type']), type_obj_data)
        return type_obj_response

    def getallobjects(self):
        """Collect objects for localdb."""
        for sinobj, pluobj in self.obj_map.items():
            self.offset = 0
            local_limit = 500
            objs_data = {'limit': local_limit, 'offset': self.offset}
            app.logger.info(
                'Retrieving {} from remote database. Offset:{}, Limit:{}'.
                format(pluobj, self.offset, local_limit))
            objs_result = self.api_call('show-{}'.format(pluobj), objs_data)
            for obj in objs_result.json()['objects']:
                self.dbobj.insert_object(obj)
            if objs_result.json()['total'] != 0:
                while objs_result.json()['to'] != objs_result.json()['total']:
                    self.offset += 500
                    moreobjs = {'limit': local_limit, 'offset': self.offset}
                    app.logger.info(
                        'Retrieving {} from remote database. Offset:{}, Limit:{}'.
                        format(pluobj, self.offset, local_limit))
                    objs_result = self.api_call('show-{}'.format(pluobj),
                                                moreobjs)
                    for obj in objs_result.json()['objects']:
                        self.dbobj.insert_object(obj)
        self.dbobj.dbconn.commit()

    def deldifobjects(self):
        local_uids = self.dbobj.local_uids()
        remote_uids = self.getalluid()
        for luid in local_uids:
            if luid not in remote_uids:
                self.dbobj.delete_object(luid)
        self.dbobj.dbconn.commit()

    def getdifobjects(self):
        """Collect objects uid for localdb comparison and add if they don't exist."""
        for sinobj, pluobj in self.obj_map.items():
            self.offset = 0
            local_limit = 500
            objs_data = {
                'limit': local_limit,
                'offset': self.offset,
                'details-level': 'uid'
            }
            objs_result = self.api_call('show-{}'.format(pluobj), objs_data)
            for obj in objs_result.json()['objects']:
                if not self.dbobj.uidcheck(obj):
                    self.getoneobject(obj, sinobj)
            if objs_result.json()['total'] != 0:
                while objs_result.json()['to'] != objs_result.json()['total']:
                    self.offset += 500
                    moreobjs = {
                        'limit': local_limit,
                        'offset': self.offset,
                        'details-level': 'uid'
                    }
                    objs_result = self.api_call('show-{}'.format(pluobj),
                                                moreobjs)
                    for obj in objs_result.json()['objects']:
                        if not self.dbobj.uidcheck(obj):
                            self.getoneobject(obj, sinobj)
        self.dbobj.dbconn.commit()

    def getoneobject(self, uid, cptype):
        """Collect single object for getdifobjects."""
        get_obj_data = {'uid': uid}
        get_obj_result = self.api_call('show-{}'.format(cptype), get_obj_data)
        self.dbobj.insert_object(get_obj_result.json())

    def countallobjects(self):
        """Count objects for local comparison"""
        # Reset count for consecutive pulls.
        self.remote_obj = 0
        for sinobj, pluobj in self.obj_map.items():
            objs_data = {'limit': 1}
            objs_result = self.api_call('show-{}'.format(pluobj), objs_data)
            if 'total' in objs_result.json():
                self.remote_obj += objs_result.json()['total']

    def getalluid(self):
        all_uids = []
        for sinobj, pluobj in self.obj_map.items():
            self.offset = 0
            local_limit = 500
            objs_data = {
                'limit': local_limit,
                'offset': self.offset,
                'details-level': 'uid'
            }
            obj_response = self.api_call('show-{}'.format(pluobj), objs_data)
            for uid in obj_response.json()['objects']:
                all_uids.append(uid)
            if obj_response.json()['total'] != 0:
                while obj_response.json()['to'] != obj_response.json()['total']:
                    self.offset += 500
                    moreobjs = {
                        'limit': local_limit,
                        'offset': self.offset,
                        'details-level': 'uid'
                    }
                    obj_response = self.api_call('show-{}'.format(pluobj),
                                                 moreobjs)
                    for uid in obj_response.json()['objects']:
                        all_uids.append(uid)
        return all_uids

    def getalllayers(self):
        """Retrieve all rule base layers from management server."""
        all_layers = []
        self.offset = 0
        get_layers_data = {'limit': self.limit, 'offset': self.offset}
        get_layers_result = self.api_call('show-access-layers',
                                          get_layers_data)
        for layer in get_layers_result.json()['access-layers']:
            all_layers.append((layer['name'], layer['uid']))

        # In case there is ever a way to have 0 layers
        if get_layers_result.json()['total'] != 0:
            while get_layers_result.json()['to'] != get_layers_result.json(
            )['total']:
                self.offset += 50
                get_more_layers = {'limit': self.limit, 'offset': self.offset}
                get_layers_result = self.api_call('show-access-layers',
                                                  get_more_layers)
                for layer in get_layers_result.json()['access-layers']:
                    all_layers.append((layer['name'], layer['uid']))

        return all_layers

    def customcommand(self, command, payload):
        """Validate payload and send command to server."""
        try:
            payload = ast.literal_eval(payload)
        except ValueError:
            return 'Invalid input provided.'
        except Exception as exc:
            return exc
        response = self.api_call(command, payload)
        return response

    def getallcommands(self):
        """Get all available commands for custom command page."""
        getcommands_result = self.api_call('show-commands', {})
        return [obj['name'] for obj in getcommands_result.json()['commands']]

    def getalltargets(self):
        """Get all gateways and servers from Check Point."""
        all_targets = []
        self.offset = 0
        get_targets_data = {'limit': self.limit, 'offset': self.offset}
        get_targets_result = self.api_call('show-gateways-and-servers',
                                           get_targets_data)
        for target in get_targets_result.json()['objects']:
            all_targets.append(target['name'])

        while get_targets_result.json()['to'] != get_targets_result.json(
        )['total']:
            self.offset += 50
            get_more_targets = {'limit': self.limit, 'offset': self.offset}
            get_targets_result = self.api_call('show-gateways-and-servers',
                                               get_more_targets)
            for target in get_targets_result.json()['objects']:
                all_targets.append(target['name'])

        return all_targets

    def runcommand(self, target, scriptcontent):
        """Issue command against Check Point targets, verify task is complete on each gateways
        and return response for each target."""
        taskreturn = []
        run_script_data = {
            'script-name': 'cpapi',
            'script': scriptcontent,
            'targets': target
        }
        response = self.api_call('run-script', run_script_data)
        if response.status_code == 200:
            if 'tasks' in response.json():
                for task in response.json()['tasks']:
                    tasktrg = task['target']
                    taskid = task['task-id']
                    taskperc = 0
                    while taskperc < 100:
                        taskresponse = self.gettask(taskid)
                        taskperc = taskresponse.json()['tasks'][0][
                            'progress-percentage']
                        if taskperc == 100:
                            if taskresponse.json()['tasks'][0]['task-details'][
                                    0]['responseMessage']:
                                base64resp = taskresponse.json()['tasks'][0][
                                    'task-details'][0]['responseMessage']
                                asciiresp = self.base64_ascii(base64resp)
                                taskreturn.append({
                                    'target':
                                    tasktrg,
                                    'status':
                                    taskresponse.json()['tasks'][0]['status'],
                                    'response':
                                    asciiresp
                                })
                            else:
                                taskreturn.append({
                                    'target':
                                    tasktrg,
                                    'status':
                                    taskresponse.json()['tasks'][0]['status'],
                                    'response':
                                    'Not Available'
                                })
                        time.sleep(1)
                return taskreturn
        elif response.status_code == 404:
            return response.text
        else:
            return response

    def gettask(self, task):
        """Function for runcommand to get task status."""
        get_task_data = {'task-id': task, 'details-level': 'full'}
        response = self.api_call('show-task', get_task_data)
        return response

    def get_local_objs(self):
        return self.dbobj.allobjects()

    def add_rule(self, ruledata):
        """Recieves rule number from form and uses lastlayer from class."""
        addruleresp = self.api_call('add-access-rule', ruledata)
        if addruleresp.status_code == 200:
            response = self.publish()
            if response.status_code != 200:
                return response.text
        else:
            return addruleresp.text

    def delete_rule(self, rulenumber):
        """Recieves rule number from form and uses lastlayer from class."""
        delruledata = {'layer': self.lastlayer, 'rule-number': rulenumber}
        delruleresp = self.api_call('delete-access-rule', delruledata)
        if delruleresp.status_code == 200:
            response = self.publish()
            if response.status_code != 200:
                return response.text
        else:
            return delruleresp.text

    def dorulebase(self, rules, rulebase):
        """Recieves json respone of showrulebase and sends rule dictionaries into
        filterpolicyrule."""
        for rule in rulebase.json()['rulebase']:
            if 'type' in rule:
                thetype = rule['type']
                if thetype == 'access-rule':
                    filteredrule = self.filterpolicyrule(rule, rulebase.json())
                    rules.append(filteredrule)
                else:
                    # Section can have no name just like rule...
                    if 'name' in rule:
                        section = rule['name']
                    else:
                        section = ''
                    rules.append({'type': 'section', 'name': section})
            if 'rulebase' in rule:
                for subrule in rule['rulebase']:
                    filteredrule = self.filterpolicyrule(
                        subrule, rulebase.json())
                    rules.append(filteredrule)
        return rules

    def showrulebase(self, layer_uid):
        """Issues API call to manager and holds response of rules until all
        filtering is complete."""
        self.offset = 0
        show_rulebase_data = {
            'uid': layer_uid,
            'details-level': 'standard',
            'offset': self.offset,
            'limit': self.limit,
            'use-object-dictionary': 'true'
        }
        app.logger.info(
            'Retrieving rules from layer:{}, offset:{}, limit:{}'.format(
                layer_uid, self.offset, self.limit))
        show_rule_result = self.api_call('show-access-rulebase',
                                         show_rulebase_data)

        rules = []

        self.dorulebase(rules, show_rule_result)
        while show_rule_result.json()['to'] != show_rule_result.json()['total']:
            self.offset += 50
            show_more_rulebase = {
                'uid': layer_uid,
                'details-level': 'standard',
                'offset': self.offset,
                'limit': self.limit,
                'use-object-dictionary': 'true'
            }
            app.logger.info(
                'Retrieving rules from layer:{}, offset:{}, limit:{}'.format(
                    layer_uid, self.offset, self.limit))
            show_rule_result = self.api_call('show-access-rulebase',
                                             show_more_rulebase)
            self.dorulebase(rules, show_rule_result)

        return rules

    @staticmethod
    def filterpolicyrule(rule, show_rulebase_result):
        """The actual filtering of a rule."""
        filteredrule = {}
        if 'name' in rule:
            name = rule['name']
        else:
            name = ''
        num = rule['rule-number']
        src = rule['source']
        src_all = []
        dst = rule['destination']
        dst_all = []
        srv = rule['service']
        srv_all = []
        act = rule['action']
        if rule['track']['type']:
            trc = rule['track']['type']
        else:
            trc = rule['track']
        trg = rule['install-on']
        trg_all = []
        for obj in show_rulebase_result['objects-dictionary']:
            if name == obj['uid']:
                name = obj['name']
            if num == obj['uid']:
                num = obj['name']
            if act == obj['uid']:
                act = obj['name']
            if trc == obj['uid']:
                trc = obj['name']
        for srcobj in src:
            for obj in show_rulebase_result['objects-dictionary']:
                if srcobj == obj['uid']:
                    src_all.append((obj['name'], srcobj))
        for dstobj in dst:
            for obj in show_rulebase_result['objects-dictionary']:
                if dstobj == obj['uid']:
                    dst_all.append((obj['name'], dstobj))
        for srvobj in srv:
            for obj in show_rulebase_result['objects-dictionary']:
                if srvobj == obj['uid']:
                    srv_all.append((obj['name'], srvobj))
        for trgobj in trg:
            for obj in show_rulebase_result['objects-dictionary']:
                if trgobj == obj['uid']:
                    trg_all.append((obj['name'], trgobj))
        filteredrule.update({
            'type': 'rule',
            'number': num,
            'name': name,
            'source': src_all,
            'source-negate': rule['source-negate'],
            'destination': dst_all,
            'destination-negate': rule['destination-negate'],
            'service': srv_all,
            'service-negate': rule['service-negate'],
            'action': act,
            'track': trc,
            'target': trg_all,
            'enabled': rule['enabled']
        })
        return filteredrule
