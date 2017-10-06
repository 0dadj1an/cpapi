from cap.post import api_call

def addhost(ipaddress, hostname, hostip, sid):
    new_host_data = {'name':hostname, 'ipv4-address':hostip}
    response = api_call(ipaddress, 443,'add-host', new_host_data ,sid)
    return(response)

def importhosts(ipaddress, filename, sid):
    report = []
    csvhosts = open(filename, 'r').read().split('\n')
    for line in csvhosts:
        if not line:
            continue
        apiprep = line.split(';')
        response = addhost(ipaddress, apiprep[0], apiprep[1], sid)
        if response.status_code == 200:
            report.append('Host:{} - SUCCESS'.format(apiprep[0]))
        else:
            report.append('Host:{} - FAILURE'.format(apiprep[0]))
    return(report)

def getallhosts(ipaddress, sid):
    count = 500
    show_hosts_data = {'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_hosts_result = api_call(ipaddress, 443, 'show-hosts', show_hosts_data ,sid)
    allhostlist = []
    for hosts in show_hosts_result.json()["objects"]:
        allhostlist.append(hosts["name"])
    if 'to' in show_hosts_result:
        while show_hosts_result.json()["to"] != show_hosts_result.json()["total"]:
            show_hosts_data = {'offset':count, 'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
            show_hosts_result = api_call(ipaddress, 443, 'show-hosts', show_hosts_data ,sid)
            for hosts in show_hosts_result.json()["objects"]:
                allhostlist.append(hosts["name"])
            count = count + 500
    return (allhostlist)
