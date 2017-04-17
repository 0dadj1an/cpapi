class session:

    #Method to login over api
    def login(usrdef_sship, usrdef_username, usrdef_pass):
        payload = {'user':usrdef_username, 'password' : usrdef_pass}
        response = ac(usrdef_sship, 443, 'login', payload, '')
        sid = (response["sid"])
        return (sid)

    #Method to publish api session
    def publish(usrdef_sship, sid):
        publish_result = ac(usrdef_sship, 443, 'publish', {} , sid)

    #Method to discard api changes
    def discard(usrdef_sship, sid):
        discard_result = ac(usrdef_sship, 443, 'discard', {}, sid)

    #Method to logout over api
    def logout(usrdef_sship, sid):
        logout_result = ac(usrdef_sship, 443,"logout", {}, sid)
