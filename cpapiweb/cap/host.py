from cap.post import api_call
import threading, time

def addhost(ipaddress, hostname, hostip, sid):
    new_host_data = {'name':hostname, 'ipv4-address':hostip}
    response = api_call(ipaddress, 443,'add-host', new_host_data ,sid)
    return(response)

def importaddhost(ipaddress, hostname, hostip, sid):
    new_host_data = {'name':hostname, 'ipv4-address':hostip}
    addhostthread = threading.Thread(target=api_call, args=(ipaddress, 443,'add-host', new_host_data ,sid))
    addhostthread.start()
    time.sleep(0.5)

def importhosts(ipaddress, filename, sid):
    csvhosts = open(filename, 'r').read().split('\n')
    for line in csvhosts:
        if not line:
            continue
        apiprep = line.split(';')
        importaddhost(ipaddress, apiprep[0], apiprep[1], sid)
