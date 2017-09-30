from cap.post import api_call

def addnetwork(ipaddress, netname, netsub, netmask, sid):
    new_network_data = {'name':netname, 'subnet':netsub, 'subnet-mask':netmask}
    response = api_call(ipaddress, 443,'add-network', new_network_data ,sid)
    return(response)
