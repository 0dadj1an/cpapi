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
