from cap.post import api_call

def login(ipaddress, username, password, domain=None):
    if domain == None:
        payload = {'user':username, 'password' : password}
        response = api_call(ipaddress, 443, 'login', payload, sid=None)
    else:
        payload = {'user':username, 'password' : password, 'domain':domain}
        response = api_call(ipaddress, 443, 'login', payload, sid=None)
        if 'sid' in response:
            return(response)
        else:
            return('error')
