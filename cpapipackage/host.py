#Import Post
from cpapipackage.post import api_call
import threading, time, json

#Method for adding a host object
def addhost(usrdef_sship, hostname, hostip, hostcolor, sid):
    #Form API Payload and Call Post
    new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
    api_call(usrdef_sship, 443,'add-host', new_host_data ,sid)

#Method to add host to group
def addhostgroup(usrdef_sship, hostname, groupname, sid):
    #Form API Payload and Call Post
    addhostgroup_data = {'name':hostname, 'groups':groupname}
    api_call(usrdef_sship, 443,'set-host', addhostgroup_data, sid)

#Method to retrieve all hosts
def getallhosts(usrdef_sship, sid):
    #Variable for offset for more than 500 objects
    count = 500
    #Form API Payload and Call Post
    show_hosts_data = {'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
    #List to append host names to for gui display
    allhostlist = []
    #Iterate of json response for host name
    for hosts in show_hosts_result["objects"]:
        allhostlist.append(hosts["name"])
    #Continue until all objects retrieved
    if 'to' in show_hosts_result:
        while show_hosts_result["to"] != show_hosts_result["total"]:
            show_hosts_data = {'offset':count, 'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
            show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
            for host in show_hosts_result["objects"]:
                allhostlist.append(hosts["name"])
            count = count + 500
    return (allhostlist)

#Method for adding a host object for importhost
def importaddhost(usrdef_sship, hostname, hostip, hostcolor, natset, sid):
    #natset is a string coming in, evaluate to dictionary
    natset = eval(natset)
    #Form API Payload and Call Post
    new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor, 'nat-settings':natset}
    #Thread for adding 2 per second, trouble with higher speeds
    t1 = threading.Thread(target=api_call, args=(usrdef_sship, 443,'add-host', new_host_data ,sid))
    t1.start()
    time.sleep(0.5)

#Method to import host from csv file
def importhosts(usrdef_sship, filename, sid):
    csvhosts = open(filename, "r").read().split("\n")
    #Read csv and format for add command
    for line in csvhosts:
        #Not sure why this is here, probably simple...
        if not line:
            continue
        apiprep = line.split(';')
        importaddhost(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], sid)

#Method to export host to csv file
def exporthosts(usrdef_sship, sid):
    #Variable for offset for more than 500 objects
    count = 500
    #Form API Payload and Call Post
    show_hosts_data = {'offset':0, 'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
    show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
    #Write json response to log file
    hostexportfile = open(("exportedhosts.csv"), "w+")
    #Iterate over host and retrieve values to write to file
    for host in show_hosts_result["objects"]:
        #Check for ipv6 object
        if 'ipv6-address' in host:
            continue
        #Must check for NAT settings first
        if 'nat-settings' in host:
            #Save natsettings to variable to convert to string later
            natsettings = host["nat-settings"]
            #Is dictionary, save as string for write
            natsettings = str(natsettings)
        hostexportfile.write(host["name"] + ";" + host["ipv4-address"] + ";" + host["color"] + ";")
        hostexportfile.write(natsettings)
        hostexportfile.write("\n")
    #Continue until all objects retrieved
    if 'to' in show_hosts_result:
        while show_hosts_result["to"] != show_hosts_result["total"]:
            show_hosts_data = {'offset':count, 'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
            show_hosts_result = api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
            for host in show_hosts_result["objects"]:
                if 'ipv6-address' in host:
                    continue
                if 'nat-settings' in host:
                    natsettings = host["nat-settings"]
                    natsettings = str(natsettings)
                hostexportfile.write(host["name"] + ";" + host["ipv4-address"] + ";" + host["color"] + ";")
                hostexportfile.write(natsettings)
                hostexportfile.write("\n")
            count = count + 500
    hostexportfile.close()
