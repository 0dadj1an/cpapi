from cap.post import api_call

class APISession:

    def __init__(self):
        pass

    def login(self, ipaddress, username, password, domain=None):
        """Login to Check Point API."""
        if domain == None:
            payload = {'user':username, 'password' : password}
            response = api_call(ipaddress, 443, 'login', payload, sid=None)
        else:
            payload = {'user':username, 'password' : password, 'domain':domain}
            response = api_call(ipaddress, 443, 'login', payload, sid=None)
        if response.status_code == 200:
            self.ipaddress = ipaddress
            self.sid = response.json()['sid']
        elif response.status_code == 400:
            return response.text
        else:
            return response

    def publish(self):
        '''Publish changes to Check Point.'''
        response = api_call(self.ipaddress, 443, 'publish', {} , self.sid)
        return response

    def discard(self):
        '''Discard changes to Check Point.'''
        response = api_call(self.ipaddress, 443, 'discard', {}, self.sid)
        return response

    def logout(self):
        '''Logout of Check Point.'''
        response = api_call(self.ipaddress, 443,"logout", {}, self.sid)
        return response
