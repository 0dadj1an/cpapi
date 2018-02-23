from cap.post import api_call

def addnetwork(ipaddress, netname, netsub, netmask, sid):
    '''Add individual network object.'''
    new_network_data = {'name':netname, 'subnet':netsub, 'subnet-mask':netmask}
    response = api_call(ipaddress, 443,'add-network', new_network_data ,sid)
    return(response)

def importnetworks(ipaddress, filename, sid):
    '''Filter CSV import file and submit networks indivually to addnetwork.'''
    report = []
    csvnets = open(filename, 'r').read().split('\n')
    for line in csvnets:
        if not line:
            continue
        apiprep = line.split(';')
        response = addnetwork(ipaddress, apiprep[0], apiprep[1], apiprep[2], sid)
        if response.status_code == 200:
            report.append('Network:{} - SUCCESS'.format(apiprep[0]))
        else:
            report.append('Network:{} - FAILURE'.format(apiprep[0]))
    return(report)

def getallnetworks(ipaddress, sid):
    '''Retrieve all networks by name from Check Point.'''
    count = 500
    show_nets_data = {'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_nets_result = api_call(ipaddress, 443, 'show-networks', show_nets_data, sid)
    allnetlist = []
    for nets in show_nets_result.json()["objects"]:
        allnetlist.append(nets["name"])
    if 'to' in show_nets_result:
        while show_nets_result.json()["to"] != show_nets_result.json()["total"]:
            show_nets_data = {'offset':count, 'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
            show_nets_result = api_call(ipaddress, 443, 'show-networks', show_nets_data ,sid)
            for nets in show_nets_result.json()["objects"]:
                allnetlist.append(nets["name"])
            count = count + 500
    return (allnetlist)
