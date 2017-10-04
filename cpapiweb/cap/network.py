from cap.post import api_call
import threading, time

def addnetwork(ipaddress, netname, netsub, netmask, sid):
    new_network_data = {'name':netname, 'subnet':netsub, 'subnet-mask':netmask}
    response = api_call(ipaddress, 443,'add-network', new_network_data ,sid)
    return(response)

def importaddnetwork(ipaddress, netname, netsub, netmask, sid):
    new_network_data = {'name':netname, 'subnet':netsub, 'subnet-mask':netmask}
    addnetthread = threading.Thread(target=api_call, args=(ipaddress, 443,'add-network', new_network_data ,sid))
    addnetthread.start()
    time.sleep(0.5)

def importnetworks(ipaddress, filename, sid):
    csvnets = open(filename, 'r').read().split('\n')
    for line in csvnets:
        if not line:
            continue
        apiprep = line.split(';')
        importaddnetwork(ipaddress, apiprep[0], apiprep[1], apiprep[2], sid)
