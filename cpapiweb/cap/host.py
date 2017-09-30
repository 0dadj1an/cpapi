from cap.post import api_call

def addhost(ipaddress, hostname, hostip, sid):
    new_host_data = {'name':hostname, 'ipv4-address':hostip}
    response = api_call(ipaddress, 443,'add-host', new_host_data ,sid)
    return(response)
