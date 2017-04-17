#Import Post
from apipackage.post import api_call

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
    show_nets_data = {'offset':0, 'details-level':'standard'}
    show_nets_result = api_call(usrdef_sship, 443, 'show-networks', show_nets_data, sid)
    allnetlist = []
    for nets in show_nets_result["objects"]:
        allnetlist.append(nets["name"])
    return (allnetlist)

#Method for adding a network object for importnetworks
def importaddnetwork(usrdef_sship, netname, netsub, netmask, netcolor, natset, sid):
    natset = eval(natset)
    new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor, 'nat-settings':natset}
    api_call(usrdef_sship, 443,'add-network', new_network_data ,sid)

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
    show_networks_data = {'offset':0, 'details-level':'full'}
    show_networks_result = api_call(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
    networksexportfile = open(("exportednetworks.csv"), "w+")
    for network in show_networks_result["objects"]:
        networksexportfile = open(("exportednetworks.csv"), "a")
        if 'nat-settings' in network:
            natsettings = network["nat-settings"]
            natsettings.pop('ipv6-address', None)
            natsettings = str(natsettings)
        networksexportfile.write(network["name"] + ";" + str(network["subnet4"]) + ";" + str(network["mask-length4"]) + ";" + network["color"] + ";")
        networksexportfile.write(natsettings)
        networksexportfile.write("\n")
    networksexportfile.close()
