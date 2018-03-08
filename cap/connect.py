from cap.post import api_call


class APISession:
    def __init__(self):
        self.limit = 50
        self.offset = 0

    @staticmethod
    def login(ipaddress, username, password, domain=None):
        """Login to Check Point API."""
        if domain == None:
            payload = {
                'user': username,
                'password': password,
            }
            response = api_call(ipaddress, 443, 'login', payload, sid=None)
        else:
            payload = {
                'user': username,
                'password': password,
                'domain': domain,
            }
            response = api_call(ipaddress, 443, 'login', payload, sid=None)
        return response

    def publish(self):
        """Publish changes to Check Point."""
        response = api_call(self.ipaddress, 443, 'publish', {}, self.sid)
        return response

    def discard(self):
        """Discard changes to Check Point."""
        response = api_call(self.ipaddress, 443, 'discard', {}, self.sid)
        return response

    def keepalive(self):
        """Keepalive Check Point session."""
        response = api_call(self.ipaddress, 443, 'keepalive', {}, self.sid)
        return response

    def logout(self):
        """Logout of Check Point."""
        response = api_call(self.ipaddress, 443, "logout", {}, self.sid)
        return response
