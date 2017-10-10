from cap.post import api_call

def login(ipaddress, username, password, domain=None):
    '''Login to Check Point API.'''
    if domain == None:
        payload = {'user':username, 'password' : password}
        response = api_call(ipaddress, 443, 'login', payload, sid=None)
    else:
        payload = {'user':username, 'password' : password, 'domain':domain}
        response = api_call(ipaddress, 443, 'login', payload, sid=None)
        return(response)

def publish(ipaddress, sid):
    '''Publish changes to Check Point.'''
    response = api_call(ipaddress, 443, 'publish', {} , sid)
    return(response)

def discard(ipaddress, sid):
    '''Discard changes to Check Point.'''
    response = api_call(ipaddress, 443, 'discard', {}, sid)
    return(response)

def logout(ipaddress, sid):
    '''Logout of Check Point.'''
    response = api_call(ipaddress, 443,"logout", {}, sid)
    return(response)
