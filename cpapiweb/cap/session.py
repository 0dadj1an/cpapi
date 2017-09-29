from cap.post import api_call

def login(ipaddress, username, password, domain=None):
    if domain == None:
        payload = {'user':username, 'password' : password}
        response = api_call(ipaddress, 443, 'login', payload, '')
    else:
        payload = {'user':username, 'password' : password, 'domain':domain}
        response = api_call(ipaddress, 443, 'login', payload, '')
        if 'sid' in response:
            sid = response["sid"]
            apiver = response["api-server-version"]
            return({'sid':sid, 'apiver':apiver})
        else:
            return('error')
