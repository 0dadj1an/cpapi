import ast
import base64
import os
import time

from app import app
from app import sqlhelp

from cpapilib.Management import Management

class CheckPoint(Management):

    def verify_db(self):
        """At login, ensure local object database exists.
        If not create it via sqlhelp, also create sqlite3 connection."""
        if self.domain:
            self.localdb = '{}{}_{}.db'.format(app.config['BASEDIR'],
                                               self.host, self.domain)
        else:
            self.localdb = '{}{}.db'.format(app.config['BASEDIR'],
                                            self.host)
        if not os.path.exists(self.localdb):
            app.logger.info('Creating local DB {}'.format(self.localdb))
            sqlhelp.createdb(self.localdb)
        self.dbobj = sqlhelp.sqlhelper(self.localdb)

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
        self.getallcommands()
        self.getalltargets()
        self.getalllayers()

    def full_sync(self):
        """Collect objects for localdb."""
        sync = ['host', 'network', 'group', 'access-role', 'gateways-and-server']
        for cptype in sync:
            self.offset = 0
            payload = {'limit': self.max_limit, 'offset': self.offset}
            app.logger.info(
                'Retrieving {}s from remote database. Offset:{}, Limit:{}'.
                format(cptype, self.offset, self.max_limit))
            response = self.shows('host', **payload)
        # for sinobj, pluobj in self.obj_map.items():
        #     self.offset = 0
        #     local_limit = 500
        #     objs_data = {'limit': local_limit, 'offset': self.offset}
        #     app.logger.info(
        #         'Retrieving {} from remote database. Offset:{}, Limit:{}'.
        #         format(pluobj, self.offset, local_limit))
        #     objs_result = self.api_call('show-{}'.format(pluobj), objs_data)
        #     for obj in objs_result.json()['objects']:
        #         self.dbobj.insert_object(obj)
        #     if objs_result.json()['total'] != 0:
        #         while objs_result.json()['to'] != objs_result.json()['total']:
        #             self.offset += 500
        #             moreobjs = {'limit': local_limit, 'offset': self.offset}
        #             app.logger.info(
        #                 'Retrieving {} from remote database. Offset:{}, Limit:{}'.
        #                 format(pluobj, self.offset, local_limit))
        #             objs_result = self.api_call('show-{}'.format(pluobj),
        #                                         moreobjs)
        #             for obj in objs_result.json()['objects']:
        #                 self.dbobj.insert_object(obj)
        self.dbobj.dbconn.commit()

    def getallcommands(self):
        """Get all available commands for custom command page."""
        getcommands_result = self.shows('command')
        self.all_commands = [obj['name'] for obj in getcommands_result['commands']]

    def getalltargets(self):
        """Get all gateways and servers from Check Point."""
        self.all_targets = []
        self.offset = 0
        payload = {'limit': self.small_limit, 'offset': self.offset}
        response = self.shows('gateways-and-server', **payload)
        for target in response['objects']:
            self.all_targets.append(target['name'])
        while response['to'] != response['total']:
            self.offset += self.small_limit
            payload = {'limit': self.small_limit, 'offset': self.offset}
            response = self.shows('gateways-and-server', **payload)
            for target in response['objects']:
                self.all_targets.append(target['name'])

    def getalllayers(self):
        """Retrieve all rule base layers from management server."""
        self.all_layers = []
        self.offset = 0
        payload = {'limit': self.small_limit, 'offset': self.offset}
        response = self.shows('access-layer', **payload)
        for layer in response['access-layers']:
            self.all_layers.append((layer['name'], layer['uid']))
        # In case there is ever a way to have 0 layers
        if response['total'] != 0:
            while response['to'] != response['total']:
                self.offset += self.small_limit
                payload = {'limit': self.small_limit, 'offset': self.offset}
                response = self.shows('access-layer', **payload)
                for layer in response['access-layers']:
                    self.all_layers.append((layer['name'], layer['uid']))

    def customcommand(self, command, payload):
        """Validate payload and send command to server."""
        try:
            payload = ast.literal_eval(payload)
        except ValueError:
            return 'Invalid input provided.'
        except Exception as exc:
            return exc
        return self._api_call(command, **payload)

    def runcommand(self, targets, script):
        """Issue command against Check Point targets, verify task is complete
        on each gateways and return response for each target."""
        taskreturn = []
        payload = {
            'script-name': 'cpapi',
            'script': script,
            'targets': targets
        }
        response = self.command('run', 'script', **payload)
        if 'tasks' in response:
            for task in response['tasks']:
                target = task['target']
                taskid = task['task-id']
                taskresponse = self.monitortask(target, taskid)
                taskreturn.append(taskresponse)
        return taskreturn

    def monitortask(self, target, taskid):
        """Run gettask until task is complete and we can return response."""
        complete = False
        while not complete:
            response = self.gettask(taskid)
            if response['tasks'][0]['progress-percentage'] == 100:
                complete = True
                if response['tasks'][0]['task-details'][0]['responseMessage']:
                    base64resp = response['tasks'][0]['task-details'][0]['responseMessage']
                    asciiresp = self.base64_ascii(base64resp)
                    return {
                        'target': target,
                        'status': response['tasks'][0]['status'],
                        'response': asciiresp
                    }
                else:
                    return {
                        'target': target,
                        'status': response['tasks'][0]['status'],
                        'response': 'Not Available'
                    }
            time.sleep(1)

    def gettask(self, task):
        """Get individual task information."""
        payload = {'task-id': task, 'details-level': 'full'}
        return self.show('task', **payload)

    @staticmethod
    def base64_ascii(base64resp):
        """Converts base64 to ascii for run command/showtask."""
        return base64.b64decode(base64resp).decode('utf-8')
