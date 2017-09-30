from cap.post import api_call

def login(ipaddress, username, password, domain=None):
    if domain == None:
        payload = {'user':username, 'password' : password}
        response = api_call(ipaddress, 443, 'login', payload, sid=None)
    else:
        payload = {'user':username, 'password' : password, 'domain':domain}
        response = api_call(ipaddress, 443, 'login', payload, sid=None)
        return(response)

def publish(ipaddress, sid):
    response = api_call(ipaddress, 443, 'publish', {} , sid)
    return(response)

#Method to discard api changes
def discard(ipaddress, sid):
    response = api_call(ipaddress, 443, 'discard', {}, sid)
    return(response)

#Method to logout over api
def logout(ipaddress, sid):
    response = api_call(ipaddress, 443,"logout", {}, sid)
    return(response)
