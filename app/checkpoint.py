import ast

from cpapilib.Management import Management

class CheckPoint(Management):

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
        return self.api_call(command, **payload)
