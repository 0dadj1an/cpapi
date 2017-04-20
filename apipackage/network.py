#Import Post
from apipackage.post import api_call
import threading, time

#Method for adding a network object
def addnetwork(usrdef_sship, netname, netsub, netmask, netcolor, sid):
    new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor}
    api_call(usrdef_sship, 443,'add-network', new_network_data ,sid)

#Method to add network to group
def addnetgroup(usrdef_sship, netname, groupname, sid):
    addnetgroup_data = {'name':netname, 'groups':groupname}
    api_call(usrdef_sship, 443, 'set-network', addnetgroup_data, sid)

#Method to retrieve all networks
def getallnetworks(usrdef_sship, sid):
    count = 500
    show_nets_data = {'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_nets_result = api_call(usrdef_sship, 443, 'show-networks', show_nets_data, sid)
    allnetlist = []
    for nets in show_nets_result["objects"]:
        allnetlist.append(nets["name"])
    while show_nets_result["to"] != show_nets_result["total"]:
        show_nets_data = {'offset':count, 'limit':500, 'details-level':'standard'}
        show_nets_result = api_call(usrdef_sship, 443, 'show-networks', show_nets_data ,sid)
        for nets in show_nets_result["objects"]:
            allnetlist.append(nets["name"])
        count = count + 500
    return (allnetlist)

#Method for adding a network object for importnetworks
def importaddnetwork(usrdef_sship, netname, netsub, netmask, netcolor, natset, sid):
    natset = eval(natset)
    new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor, 'nat-settings':natset}
    t1 = threading.Thread(target=api_call, args=(usrdef_sship, 443,'add-network', new_network_data ,sid))
    t1.start()
    time.sleep(0.1)

#Method to import networks from csv
def importnetworks(usrdef_sship, filename, sid):
    csvnets = open(filename, "r").read().split("\n")
    for line in csvnets:
        if not line:
            continue
        apiprep = line.split(';')
        importaddnetwork(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4], sid)

#Method to export host to csv file
def exportnetworks(usrdef_sship, sid):
    count = 500
    show_networks_data = {'offset':0, 'limit':500, 'details-level':'full'}
    show_networks_result = api_call(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
    networksexportfile = open(("exportednetworks.csv"), "w+")
    for network in show_networks_result["objects"]:
        if 'nat-settings' in network:
            natsettings = network["nat-settings"]
            natsettings.pop('ipv6-address', None)
            natsettings = str(natsettings)
        networksexportfile.write(network["name"] + ";" + str(network["subnet4"]) + ";" + str(network["mask-length4"]) + ";" + network["color"] + ";")
        networksexportfile.write(natsettings)
        networksexportfile.write("\n")
    while show_networks_result["to"] != show_networks_result["total"]:
        show_networks_data = {'offset':count, 'limit':500, 'details-level':'full'}
        show_networks_result = api_call(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
        for network in show_networks_result["objects"]:
            if 'nat-settings' in network:
                natsettings = network["nat-settings"]
                natsettings.pop('ipv6-address', None)
                natsettings = str(natsettings)
            networksexportfile.write(network["name"] + ";" + str(network["subnet4"]) + ";" + str(network["mask-length4"]) + ";" + network["color"] + ";")
            networksexportfile.write(natsettings)
            networksexportfile.write("\n")
        count = count + 500
    networksexportfile.close()
