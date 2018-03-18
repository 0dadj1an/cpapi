import getpass
import json
import requests

from app import app


class Management(object):

    def __init__(self, host, user, password=None, sid=None,
                 port='443', domain=None, verify=False):
        """Creation of ManagementAPI Class object.

        :param host: Check Point Managment Server
        :param user: SmartConsole User
        :param password: SmartConsole Password
        :param sid: Check Point API Session ID
        :param port: Check Point Apache Port
        :param domain: Check Point MDS Domain(optional)
        :param verify: Requests Verify SSL
        :type port: string
        """
        self.offset = 0
        self.small_limit = 50
        self.max_limit = 500
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.domain = domain
        self.sid = sid
        self.api_version = None
        self.verify = verify
        self.request_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CPAPI v{}'.format(app.config['version'])
        }

        if not verify:
            #TODO: Currently no way to pass verify=True.
            requests.packages.urllib3.disable_warnings()

    @property
    def url(self):
        """Standard URL for all Management API Calls."""
        return 'https://{}:{}/web_api/'.format(self.host, self.port)

    def _api_call(self, command, **kwargs):
        """Backbone method for sending POST to Check Point."""
        if self.sid:
            self.request_headers.update({'X-chkp-sid': self.sid})
        try:
            app.logger.debug('Command Issued: {}'.format(command))
            response = requests.post(
                self.url + command,
                data=json.dumps(kwargs),
                headers=self.request_headers,
                timeout=(15, 300),
                verify=self.verify)
        except requests.exceptions.RequestException as e:
            app.logger.error('{} : {}'.format(type(e).__name__, e))
        if str(response.status_code)[0] == '2':
            app.logger.debug('Command Success: {}'.format(command))
            return response.json()
        elif str(response.status_code)[0] =='4':
            app.logger.warn('Command Failure: {}'.format(command))
            app.logger.warn(response.text)
            return response.text
        elif str(response.status_code)[0] == '5':
            app.logger.error('Server Failure: {}'.format(command))
            app.logger.error(response)
            return response.text

    def login(self):
        if not self.password:
            self.password = getpass.getpass('Password >> ')
        payload = {
            'user': self.user,
            'password': self.password,
        }
        if self.domain:
            payload.update({'domain': self.domain})
        response = self._api_call('login', **payload)
        if 'sid' in response:
            self.sid = response['sid']
            self.api_version = response['api-server-version']
        return response

    def publish(self, **kwargs):
        return self._api_call('publish', **kwargs)

    def discard(self, **kwargs):
        return self._api_call('discard', **kwargs)

    def logout(self, **kwargs):
        response = self._api_call('logout', **kwargs)
        if response['message'] == 'OK':
            self.sid = None
        return response

    def keepalive(self, **kwargs):
        return self._api_call('keepalive', **kwargs)

    def export(self, **kwargs):
        return self._api_call('export', **kwargs)

    def process(self, action, **kwargs):
        return getattr(self, action, **kwargs)

    def command(self, action, cptype, **kwargs):
        return getattr(self, action)(cptype, **kwargs)

    def add(self, cptype, **kwargs):
        return self._api_call('add-{}'.format(cptype), **kwargs)

    def set(self, cptype, **kwargs):
        return self._api_call('set-{}'.format(cptype), **kwargs)

    def delete(self, cptype, **kwargs):
        return self._api_call('delete-{}'.format(cptype), **kwargs)

    def show(self, cptype, **kwargs):
        return self._api_call('show-{}'.format(cptype), **kwargs)

    def shows(self, cptype, **kwargs):
        return self._api_call('show-{}s'.format(cptype), **kwargs)

    def policy(self, action, **kwargs):
        """Unique to policy verification and installation."""
        return self._api_call('{}-policy'.format(action), **kwargs)

    def run(self, task, **kwargs):
        """Unique to script and ips-update."""
        return self._api_call('run-{}'.format(task), **kwargs)

    def unlock(self, **kwargs):
        """Unique to administrators."""
        return self._api_call('unlock-administrator', **kwargs)

    def whereused(self, **kwargs):
        return self._api_call('where-used', **kwargs)
