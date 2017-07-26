#Import Post
from cpapipackage.post import api_call

#Method to login over api
def login(usrdef_sship, usrdef_username, usrdef_pass, domain=None):
    if domain == None:
        payload = {'user':usrdef_username, 'password' : usrdef_pass}
        response = api_call(usrdef_sship, 443, 'login', payload, '')
    else:
        payload = {'user':usrdef_username, 'password' : usrdef_pass, 'domain':domain}
        response = api_call(usrdef_sship, 443, 'login', payload, '')
    sid = (response["sid"])
    return (sid)

#Method to publish api session
def publish(usrdef_sship, sid):
    api_call(usrdef_sship, 443, 'publish', {} , sid)

#Method to discard api changes
def discard(usrdef_sship, sid):
    api_call(usrdef_sship, 443, 'discard', {}, sid)

#Method to logout over api
def logout(usrdef_sship, sid):
    api_call(usrdef_sship, 443,"logout", {}, sid)
