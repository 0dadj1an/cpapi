#Import Post
from cpapipackage.post import api_call
import threading, time

#Method for adding a network object
def addnetwork(usrdef_sship, netname, netsub, netmask, netcolor, sid):
    #Form API Payload and Call Post
    new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor}
    api_call(usrdef_sship, 443,'add-network', new_network_data ,sid)

#Method to add network to group
def addnetgroup(usrdef_sship, netname, groupname, sid):
    #Form API Payload and Call Post
    addnetgroup_data = {'name':netname, 'groups':groupname}
    api_call(usrdef_sship, 443, 'set-network', addnetgroup_data, sid)

#Method to retrieve all networks
def getallnetworks(usrdef_sship, sid):
    #Variable for offset for more than 500 objects
    count = 500
    #Form API Payload and Call Post
    show_nets_data = {'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_nets_result = api_call(usrdef_sship, 443, 'show-networks', show_nets_data, sid)
    #List to append newtork to
    allnetlist = []
    #Iterate over json response for network name only
    for nets in show_nets_result["objects"]:
        allnetlist.append(nets["name"])
    #Continue until all objects retrieved
    if 'to' in show_nets_result:
        while show_nets_result["to"] != show_nets_result["total"]:
            show_nets_data = {'offset':count, 'limit':500, 'details-level':'standard'}
            show_nets_result = api_call(usrdef_sship, 443, 'show-networks', show_nets_data ,sid)
            for nets in show_nets_result["objects"]:
                allnetlist.append(nets["name"])
            count = count + 500
    return (allnetlist)

#Method for adding a network object for importnetworks
def importaddnetwork(usrdef_sship, netname, netsub, netmask, netcolor, natset, sid):
    #natset comes in as string, eval for dictionary
    natset = eval(natset)
    #Form API Payload and Call Post
    new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor, 'nat-settings':natset}
    #Thread for 2 api call per second
    #Had problems with faster threading
    #On low end machines
    t1 = threading.Thread(target=api_call, args=(usrdef_sship, 443,'add-network', new_network_data ,sid))
    t1.start()
    time.sleep(0.5)

#Method to import networks from csv
def importnetworks(usrdef_sship, filename, sid):
    csvnets = open(filename, "r").read().split("\n")
    #Read csv and format for add funciton
    for line in csvnets:
        #I'll figure this one out one day
        if not line:
            continue
        apiprep = line.split(';')
        importaddnetwork(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4], sid)

#Method to export host to csv file
def exportnetworks(usrdef_sship, sid):
    #Variable for offset for more than 500 objects
    count = 500
    #Form API Payload and Call Post
    show_networks_data = {'offset':0, 'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
    show_networks_result = api_call(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
    #Write json response to log file
    networksexportfile = open(("exportednetworks.csv"), "w+")
    #Iterate over json response to export network info
    for network in show_networks_result["objects"]:
        #Check for ipv6 object
        if 'subnet6' in network:
            continue
        #Have to check for NAT first
        if 'nat-settings' in network:
            #Save natsettings to variabl to modify to string later
            natsettings = network["nat-settings"]
            #Save as string for write
            natsettings = str(natsettings)
        networksexportfile.write(network["name"] + ";" + str(network["subnet4"]) + ";" + str(network["mask-length4"]) + ";" + network["color"] + ";")
        networksexportfile.write(natsettings)
        networksexportfile.write("\n")
    #Continue until all objects retrieved
    if 'to' in show_nets_result:
        while show_networks_result["to"] != show_networks_result["total"]:
            show_networks_data = {'offset':count, 'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
            show_networks_result = api_call(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
            for network in show_networks_result["objects"]:
                if 'subnet6' in network:
                    continue
                if 'nat-settings' in network:
                    natsettings = network["nat-settings"]
                    natsettings = str(natsettings)
                networksexportfile.write(network["name"] + ";" + str(network["subnet4"]) + ";" + str(network["mask-length4"]) + ";" + network["color"] + ";")
                networksexportfile.write(natsettings)
                networksexportfile.write("\n")
            count = count + 500
    networksexportfile.close()
