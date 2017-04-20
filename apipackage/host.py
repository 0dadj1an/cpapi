#Import Post
from apipackage.post import api_call
import threading, time

#Method for adding a host object
def addhost(usrdef_sship, hostname, hostip, hostcolor, sid):
    new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
    api_call(usrdef_sship, 443,'add-host', new_host_data ,sid)

#Method to add host to group
def addhostgroup(usrdef_sship, hostname, groupname, sid):
    addhostgroup_data = {'name':hostname, 'groups':groupname}
    api_call(usrdef_sship, 443,'set-host', addhostgroup_data, sid)

#Method to retrieve all hosts
def getallhosts(usrdef_sship, sid):
    count = 500
    show_hosts_data = {'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
    allhostlist = []
    for hosts in show_hosts_result["objects"]:
        allhostlist.append(hosts["name"])
    while show_hosts_result["to"] != show_hosts_result["total"]:
        show_hosts_data = {'offset':count, 'limit':500, 'details-level':'standard'}
        show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        for host in show_hosts_result["objects"]:
            allhostlist.append(hosts["name"])
        count = count + 500
    return (allhostlist)

#Method for adding a host object for importhost
def importaddhost(usrdef_sship, hostname, hostip, hostcolor, natset, sid):
    natset = eval(natset)
    new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor, 'nat-settings':natset}
    t1 = threading.Thread(target=api_call, args=(usrdef_sship, 443,'add-host', new_host_data ,sid))
    t1.start()
    time.sleep(0.1)

#Method to import host from csv file
def importhosts(usrdef_sship, filename, sid):
    csvhosts = open(filename, "r").read().split("\n")
    for line in csvhosts:
        if not line:
            continue
        apiprep = line.split(';')
        importaddhost(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], sid)

#Method to export host to csv file
def exporthosts(usrdef_sship, sid):
    count = 500
    show_hosts_data = {'offset':0, 'limit':500, 'details-level':'full'}
    show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
    hostexportfile = open(("exportedhosts.csv"), "w+")
    for host in show_hosts_result["objects"]:
        if 'nat-settings' in host:
            natsettings = host["nat-settings"]
            natsettings.pop('ipv6-address', None)
            natsettings = str(natsettings)
        hostexportfile.write(host["name"] + ";" + host["ipv4-address"] + ";" + host["color"] + ";")
        hostexportfile.write(natsettings)
        hostexportfile.write("\n")
    while show_hosts_result["to"] != show_hosts_result["total"]:
        show_hosts_data = {'offset':count, 'limit':500, 'details-level':'full'}
        show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        for host in show_hosts_result["objects"]:
            if 'nat-settings' in host:
                natsettings = host["nat-settings"]
                natsettings.pop('ipv6-address', None)
                natsettings = str(natsettings)
            hostexportfile.write(host["name"] + ";" + host["ipv4-address"] + ";" + host["color"] + ";")
            hostexportfile.write(natsettings)
            hostexportfile.write("\n")
        count = count + 500
    hostexportfile.close()
