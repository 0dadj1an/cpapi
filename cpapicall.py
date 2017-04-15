#Import Things
import sys, time, json
#Import Requests
import requests
#Import Messagebox
from tkinter import messagebox

#Global Variables
sid = "tbd"
usrdef_sship = "tbd"

class allcalls:

    #Method to carry webapi call
    def api_call(ip_addr, port, command, json_payload, sid):
        url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
        if sid == '':
            request_headers = {'Content-Type' : 'application/json'}
        else:
            request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
        r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
        return (r.json())

    #Method to login over api
    def login(ip, usrdef_username, usrdef_pass):
        payload = {'user':usrdef_username, 'password' : usrdef_pass}
        response = allcalls.api_call(ip, 443, 'login', payload, '')
        global usrdef_sship
        usrdef_sship = ip
        global sid
        #Return Error Message if sid does not exist
        if 'sid' not in response:
            messagebox.showinfo("Login Response", response["message"])
        elif 'sid' in response:
            messagebox.showinfo("Login Response", "Login Successful")
            sid = (response["sid"])
        ### CURRENTLY NOT WORKING ###
        else:
            messagebox.showinfo("Login Response", "Connection Failed")

    #Method to publish api session
    def publish():
        publish_result = allcalls.api_call(usrdef_sship, 443, 'publish', {} ,sid)
        #Return Successful if task-id exist
        if 'task-id' in publish_result:
            messagebox.showinfo("Publish Response", "Publish Successful")
        else:
            messagebox.showinfo("Publish Response", "Publish Failed")

    #Method to logout over api
    def logout():
        logout_result = allcalls.api_call(usrdef_sship, 443,"logout", {},sid)
        messagebox.showinfo("Logout Response", logout_result)

    #Method for adding a host object
    def addhost(hostname, hostip, hostcolor):
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
        new_host_result = allcalls.api_call(usrdef_sship, 443,'add-host', new_host_data ,sid)
        if 'creator' in new_host_result:
            messagebox.showinfo("Add Host Response", "Add Host Successful")
        else:
            messagebox.showinfo("Add Host Response", new_host_result)

    #Method for adding a network object
    def addnetwork(netname, netsub, netmask, netcolor):
        new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor}
        new_network_result = allcalls.api_call(usrdef_sship, 443,'add-network', new_network_data ,sid)
        if 'creator' in new_network_result:
            messagebox.showinfo("Add Network Response", "Successful")
        else:
            messagebox.showinfo("Add Network Response", new_network_result)

    #Method for adding a group object
    def addgroup(groupname):
        new_group_data = {'name':groupname}
        new_group_result = allcalls.api_call(usrdef_sship, 443,'add-group', new_group_data ,sid)
        if 'creator' in new_group_result:
            messagebox.showinfo("Add Group Response", "Successful")
        else:
            messagebox.showinfo("Add Group Response", new_group_result)

    #Method to add host to group
    def addhostgroup(hostname, groupname):
        addhostgroup_data = {'name':hostname, 'groups':groupname}
        addhostgroup_result = allcalls.api_call(usrdef_sship, 443,'set-host', addhostgroup_data, sid)
        if 'creator' in addhostgroup_result:
            messagebox.showinfo("Add Host Response", "Successful")
        else:
            messagebox.showinfo("Add Host Response", addhostgroup_result)

    #Method to add network to group
    def addnetgroup(netname, groupname):
        addnetgroup_data = {'name':netname, 'groups':groupname}
        addnetgroup_result = allcalls.api_call(usrdef_sship, 443, 'set-network', addnetgroup_data, sid)
        if 'creator' in addnetgroup_result:
            messagebox.showinfo("Add Network Response", "Successful")
        else:
            messagebox.showinfo("Add Network Response", addnetgroup_result)

    #Method to add group to group
    def addgroupgroup(addgroupname, groupname):
        addgroup_data = {'name':addgroupname, 'groups':groupname}
        addgroupgroup_result = allcalls.api_call(usrdef_sship, 443, 'set-group', addgroup_data, sid)
        if 'creator' in addgroupgroup_result:
            messagebox.showinfo("Add Group Response", "Successful")
        else:
            messagebox.showinfo("Add Group Response", addgroupgroup_result)

    #Method for retrieving objects
    def getallhosts():
        show_hosts_data = {'offset':0, 'details-level':'standard'}
        show_hosts_result = allcalls.api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        return (show_hosts_result)
    def getallgroups():
        show_groups_data = {'offset':0, 'details-level':'standard'}
        show_groups_result = allcalls.api_call(usrdef_sship, 443, 'show-groups', show_groups_data, sid)
        return (show_groups_result)
    def getallnetworks():
        show_nets_data = {'offset':0, 'details-level':'standard'}
        show_nets_result = allcalls.api_call(usrdef_sship, 443, 'show-networks', show_nets_data, sid)
        return (show_nets_result)

    #Method for adding a host object for importhost
    def importaddhost(hostname, hostip, hostcolor, natset):
        natset = eval(natset)
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor, 'nat-settings':natset}
        new_host_result = allcalls.api_call(usrdef_sship, 443,'add-host', new_host_data ,sid)

    #Method to import host from csv file
    def importhosts(filename):
        csvhosts = open(filename, "r").read().split("\n")
        for line in csvhosts:
            apiprep = line.split(';')
            allcalls.importaddhost(apiprep[0], apiprep[1], apiprep[2], apiprep[3])
        cvshosts.close()
        messagebox.showinfo("Import Host Response", "PLACEHOLDER")

    #Method to export host to csv file
    def exporthosts():
        show_hosts_data = {'offset':0, 'details-level':'full'}
        show_hosts_result = allcalls.api_call(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        hostexportfile = open(("exportedhosts.csv"), "w+")
        for host in show_hosts_result["objects"]:
            if 'nat-settings' in host:
                natsettings = host["nat-settings"]
                natsettings.pop('ipv6-address', None)
                natsettings = str(natsettings)
            hostexportfile = open(("exportedhosts.csv"), "a")
            hostexportfile.write(host["name"] + ";" + host["ipv4-address"] + ";" + host["color"] + ";")
            hostexportfile.write(natsettings)
            hostexportfile.write("\n")
        hostexportfile.close()
        messagebox.showinfo("Export Hosts Response", "PLACEHOLDER")

    #Method for adding a network object for importnetworks
    def importaddnetwork(netname, netsub, netmask, netcolor, natset):
        natset = eval(natset)
        new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor, 'nat-settings':natset}
        new_network_result = allcalls.api_call(usrdef_sship, 443,'add-network', new_network_data ,sid)

    #Method to import networks from csv
    def importnetworks(filename):
        csvnets = open(filename, "r").read().split("\n")
        for line in csvnets:
            apiprep = line.split(';')
            allcalls.importaddnetwork(apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4])
        csvnets.close()
        messagebox.showinfo("Import Network Response", "PLACEHOLDER")

    #Method to export host to csv file
    def exportnetworks():
        show_networks_data = {'offset':0, 'details-level':'full'}
        show_networks_result = allcalls.api_call(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
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
        messagebox.showinfo("Export Network Response", "PLACEHOLDER")

    #Method for adding a group object with members
    def addgroupmembers(groupname, members):
        new_group_data = {'name':groupname, 'members':members}
        new_group_result = allcalls.api_call(usrdef_sship, 443,'add-group', new_group_data ,sid)

    #Method to import group from csv
    def importgroups(filename):
        csvgroups = open(filename, "r").read().split()
        #Parse Exported Groups File
        for line in csvgroups:
            #Split Group name from members
            groupname = line.split(',')
            #Split Members from each other
            memberlist = groupname[1].split(';')
            #Pass to api, last element in memberlist is an empty string
            allcalls.addgroupmembers(groupname[0], memberlist[0:-1])
        csvgroups.close()
        messagebox.showinfo("Import Groups Response", "PLACEHOLDER")

    #Method to export host to csv file
    def exportgroups():
        show_groups_data = {'offset':0, 'details-level':'full'}
        show_groups_result = allcalls.api_call(usrdef_sship, 443, 'show-groups', show_groups_data ,sid)
        groupsexportfile = open(("exportedgroups.csv"), "w+")
        for group in show_groups_result["objects"]:
            groupsexportfile.write(group["name"] + ",")
            listofmembers = group["members"]
            for member in listofmembers:
                groupsexportfile.write(member["name"] + ";")
            groupsexportfile.write("\n")
        groupsexportfile.close()
        messagebox.showinfo("Export Groups Response", "PLACEHOLDER")

    #Method to add rule for importrules
    def importaddrules(num, name, src, dst, srv, act):
        add_rule_data = {'layer':'Network', 'position':num, 'name':name, 'source':src, 'destination':dst, 'service':srv, 'action':act}
        add_rule_result = allcalls.api_call(usrdef_sship, 443, 'add-access-rule', add_rule_data, sid)

    #Method to import rulebase from csv
    def importrules(filename):
        csvrules = open(filename, "r").read().split("\n")
        #Parse Exported Rules File
        for line in csvrules:
            #Split Rule Fields
            fullrule = line.split(',')
            num = fullrule[0]
            name = fullrule[1]
            try:
                src = fullrule[2].split(';')
            except:
                src = fullrule[2]
            try:
                dst = fullrule[3].split(';')
            except:
                dst = fullrule[3]
            try:
                srv = fullrule[4].split(';')
            except:
                srv = fullrule[4]
            act = fullrule[5]
            allcalls.importaddrules(num, name, src, dst, srv, act)
        csvrules.close()
        messagebox.showinfo("Import Rules Response", "PLACEHOLDER")

    #Method to get packages
    def getallpackages():
        get_packages_data = {'offset':0, 'details-level':'full'}
        get_packages_result = allcalls.api_call(usrdef_sship, 443, 'show-packages', get_packages_data, sid)
        return (get_packages_result)

    def getalllayers():
        get_layers_data = {'name':package}
        get_layers_result = allcalls.api_call(usrdef_sship, 443, 'show-package', get_layers_data, sid)
        return (get_layers_result)

    #Method to get export rules
    def exportrules(package, layer):
        #Retrieve Rulebase
        show_rulebase_data = {"offset":0, "package":package, "name":layer, "details-level":"standard", "use-object-dictionary":"true"}
        show_rulebase_result = allcalls.api_call(usrdef_sship, 443, 'show-access-rulebase', show_rulebase_data ,sid)
        #Create Output File
        rulebaseexport = open(("exportedrules.csv"), "w+")
        #Parse values for each rule
        for rule in show_rulebase_result["rulebase"]:
            countersrc = 0
            counterdst = 0
            countersrv = 0
            #String, String, List, List, List, String
            ### NAME CAN BE EMPTY ###
            if 'name' in rule:
                name = rule["name"]
            else:
                name = "ASSIGN NAME"
            num = rule["rule-number"]
            src = rule["source"]
            dst = rule["destination"]
            srv = rule["service"]
            act = rule["action"]
            #Parse Object Ditcionary to replace UID with Name
            for obj in show_rulebase_result["objects-dictionary"]:
                if name == obj["uid"]:
                    name = obj["name"]
            #Parse Object Ditcionary to replace UID with Name
            for obj in show_rulebase_result["objects-dictionary"]:
                if num == obj["uid"]:
                    num = obj["name"]
            #Parse Object Ditcionary to replace UID with Name: Source
            if len(src) == 1:
                for obj in show_rulebase_result["objects-dictionary"]:
                    if src[0] == obj["uid"]:
                        src = obj["name"]
            else:
                for srcobj in src:
                    for obj in show_rulebase_result["objects-dictionary"]:
                        if srcobj == obj["uid"]:
                            src[countersrc] = obj["name"]
                            countersrc = countersrc + 1
            #Parse Object Ditcionary to replace UID with Name: Destination
            if len(dst) == 1:
                for obj in show_rulebase_result["objects-dictionary"]:
                    if dst[0] == obj["uid"]:
                        dst = obj["name"]
            else:
                for dstobj in dst:
                    for obj in show_rulebase_result["objects-dictionary"]:
                        if dstobj == obj["uid"]:
                            dst[counterdst] = obj["name"]
                            counterdst = counterdst + 1
            #Parse Object Ditcionary to replace UID with Name: Service
            if len(srv) == 1:
                for obj in show_rulebase_result["objects-dictionary"]:
                    if srv[0] == obj["uid"]:
                        srv = obj["name"]
            else:
                for srvobj in srv:
                    for obj in show_rulebase_result["objects-dictionary"]:
                        if srvobj == obj["uid"]:
                            srv[countersrv] = obj["name"]
                            countersrv = countersrv + 1
            #Parse Object Ditcionary to replace UID with Name
            for obj in show_rulebase_result["objects-dictionary"]:
                if act == obj["uid"]:
                    act = obj["name"]
            #Write Rule Number and Name
            rulebaseexport.write(str(num) + ',' + name + ',')
            #Write Source, delimit multiple with ;
            if isinstance(src, str) == True:
                rulebaseexport.write(src + ',')
            else:
                for srcele in src[0:-1]:
                    rulebaseexport.write(srcele + ';')
                rulebaseexport.write(src[-1] + ',')
            #Write Destination, delimit multiple with ;
            if isinstance(dst, str) == True:
                rulebaseexport.write(dst + ',')
            else:
                for dstele in dst[0:-1]:
                    rulebaseexport.write(dstele + ';')
                rulebaseexport.write(dst[-1] + ',')
            #Write Service, delimit multiple with ;
            if isinstance(srv, str) == True:
                rulebaseexport.write(srv + ',')
            else:
                for srvele in srv[0:-1]:
                    rulebaseexport.write(srvele + ';')
                rulebaseexport.write(srv[-1] + ',')
            #Write Action and \n
            rulebaseexport.write(act + '\n')
        rulebaseexport.close()
        messagebox.showinfo("Export Rulebase", "PLACEHOLDER")

    def getalltargets():
        #Retrieve Targets
        get_targets_data = {'offset':0}
        get_targets_result = allcalls.api_call(usrdef_sship, 443, 'show-gateways-and-servers', get_targets_data ,sid)
        return (get_targets_result)

    #Method to run command
    def runscript(target, name, command):
        run_script_data = {'script-name':name, 'script':command, 'targets':target}
        get_targets_result = allcalls.api_call(usrdef_sship, 443, 'run-script', run_script_data , sid)
        for line in get_targets_result["tasks"]:
            taskid = line["task-id"]
        time.sleep(5)
        taskid_data = {'task-id':taskid, 'details-level':'full'}
        taskid_result = allcalls.api_call(usrdef_sship, 443, 'show-task', taskid_data , sid)
        for line in taskid_result["tasks"]:
            taskresult = line["task-details"][0]["statusDescription"]
        messagebox.showinfo("Run Script Output", taskresult)

    #Method to run command
    def putfile(target, path, name, contents):
        put_file_data = {'file-path':path, 'file-name':name, 'file-content':contents, 'targets':target}
        put_file_result = allcalls.api_call(usrdef_sship, 443, 'put-file', put_file_data , sid)
        messagebox.showinfo("Put File Respons", put_file_result)

    #Method to search for ip in nat settings
    def findnat(ip):
        all_hosts_data = {'offset':0, 'details-level':'full'}
        all_hosts_result = allcalls.api_call(usrdef_sship, 443, 'show-hosts', all_hosts_data, sid)
        for nat in all_hosts_result["objects"]:
            if 'ipv4-address' in nat["nat-settings"]:
                host = nat["name"]
                found = nat["nat-settings"]["ipv4-address"]
                if ip == found:
                    messagebox.showinfo("Results", ("Host: %s - contains the NAT IP" % host))
        all_networks_data = {'offset':0, 'details-level':'full'}
        all_networks_result = allcalls.api_call(usrdef_sship, 443, 'show-networks', all_networks_data, sid)
        for nat in all_networks_result["objects"]:
            if 'ipv4-address' in nat["nat-settings"]:
                network = nat["name"]
                found = nat["nat-settings"]["ipv4-address"]
                if ip == found:
                    messagebox.showinfo("Results", ("Network: %s - contains the NAT IP" % network))
