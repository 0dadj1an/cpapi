from cap.post import api_call

def addnetwork(ipaddress, netname, netsub, netmask, sid):
    new_network_data = {'name':netname, 'subnet':netsub, 'subnet-mask':netmask}
    response = api_call(ipaddress, 443,'add-network', new_network_data ,sid)
    return(response)

def importnetworks(ipaddress, filename, sid):
    report = []
    csvnets = open(filename, 'r').read().split('\n')
    for line in csvnets:
        if not line:
            continue
        apiprep = line.split(';')
        response = addnetwork(ipaddress, apiprep[0], apiprep[1], apiprep[2], sid)
        if response.status_code == 200:
            report.append('Host:{} - SUCCESS'.format(apiprep[0]))
        else:
            report.append('Host:{} - FAILURE'.format(apiprep[0]))
    return(report)
