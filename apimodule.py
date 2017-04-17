#Import Things
import sys, time
#Import Messagebox
from post import api_call as ac

class session:

    #Method to login over api
    def login(usrdef_sship, usrdef_username, usrdef_pass):
        payload = {'user':usrdef_username, 'password' : usrdef_pass}
        response = ac(usrdef_sship, 443, 'login', payload, '')
        sid = (response["sid"])
        return (sid)

    #Method to publish api session
    def publish(usrdef_sship, sid):
        publish_result = ac(usrdef_sship, 443, 'publish', {} , sid)

    #Method to discard api changes
    def discard(usrdef_sship, sid):
        discard_result = ac(usrdef_sship, 443, 'discard', {}, sid)

    #Method to logout over api
    def logout(usrdef_sship, sid):
        logout_result = ac(usrdef_sship, 443,"logout", {}, sid)

class host:

    #Method for adding a host object
    def addhost(usrdef_sship, hostname, hostip, hostcolor, sid):
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
        new_host_result = ac(usrdef_sship, 443,'add-host', new_host_data ,sid)

    #Method to add host to group
    def addhostgroup(usrdef_sship, hostname, groupname, sid):
        addhostgroup_data = {'name':hostname, 'groups':groupname}
        addhostgroup_result = ac(usrdef_sship, 443,'set-host', addhostgroup_data, sid)

    #Method to retrieve all hosts
    def getallhosts(usrdef_sship, sid):
        show_hosts_data = {'offset':0, 'details-level':'standard'}
        show_hosts_result = ac(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        return (show_hosts_result)

    #Method for adding a host object for importhost
    def importaddhost(usrdef_sship, hostname, hostip, hostcolor, natset, sid):
        natset = eval(natset)
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor, 'nat-settings':natset}
        new_host_result = ac(usrdef_sship, 443,'add-host', new_host_data ,sid)

    #Method to import host from csv file
    def importhosts(usrdef_sship, filename, sid):
        csvhosts = open(filename, "r").read().split("\n")
        for line in csvhosts:
            if not line:
                continue
            apiprep = line.split(';')
            host.importaddhost(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], sid)

    #Method to export host to csv file
    def exporthosts(usrdef_sship, sid):
        show_hosts_data = {'offset':0, 'details-level':'full'}
        show_hosts_result = ac(usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
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

class network:

    #Method for adding a network object
    def addnetwork(usrdef_sship, netname, netsub, netmask, netcolor, sid):
        new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor}
        new_network_result = ac(usrdef_sship, 443,'add-network', new_network_data ,sid)

    #Method to add network to group
    def addnetgroup(usrdef_sship, netname, groupname, sid):
        addnetgroup_data = {'name':netname, 'groups':groupname}
        addnetgroup_result = ac(usrdef_sship, 443, 'set-network', addnetgroup_data, sid)

    #Method to retrieve all networks
    def getallnetworks(usrdef_sship, sid):
        show_nets_data = {'offset':0, 'details-level':'standard'}
        show_nets_result = ac(usrdef_sship, 443, 'show-networks', show_nets_data, sid)
        return (show_nets_result)

    #Method for adding a network object for importnetworks
    def importaddnetwork(usrdef_sship, netname, netsub, netmask, netcolor, natset, sid):
        natset = eval(natset)
        new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor, 'nat-settings':natset}
        new_network_result = ac(usrdef_sship, 443,'add-network', new_network_data ,sid)

    #Method to import networks from csv
    def importnetworks(usrdef_sship, filename, sid):
        csvnets = open(filename, "r").read().split("\n")
        for line in csvnets:
            if not line:
                continue
            apiprep = line.split(';')
            network.importaddnetwork(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4], sid)

    #Method to export host to csv file
    def exportnetworks(usrdef_sship, sid):
        show_networks_data = {'offset':0, 'details-level':'full'}
        show_networks_result = ac(usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
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

class group:

    #Method for adding a group object
    def addgroup(usrdef_sship, groupname, sid):
        new_group_data = {'name':groupname}
        new_group_result = ac(usrdef_sship, 443,'add-group', new_group_data ,sid)

    #Method to add group to group
    def addgroupgroup(usrdef_sship, addgroupname, groupname, sid):
        addgroup_data = {'name':addgroupname, 'groups':groupname}
        addgroupgroup_result = ac(usrdef_sship, 443, 'set-group', addgroup_data, sid)

    #Method for retrieving all groups
    def getallgroups(usrdef_sship, sid):
        show_groups_data = {'offset':0, 'details-level':'standard'}
        show_groups_result = ac(usrdef_sship, 443, 'show-groups', show_groups_data, sid)
        return (show_groups_result)

    #Method for adding a group object with members
    def addgroupmembers(usrdef_sship, groupname, members, sid):
        new_group_data = {'name':groupname, 'members':members}
        new_group_result = ac(usrdef_sship, 443,'add-group', new_group_data ,sid)

    #Method to import group from csv
    def importgroups(usrdef_sship, filename, sid):
        csvgroups = open(filename, "r").read().split()
        for line in csvgroups:
            if not line:
                continue
            groupname = line.split(',')
            memberlist = groupname[1].split(';')
            group.addgroupmembers(usrdef_sship, groupname[0], memberlist[0:-1], sid)

    #Method to export host to csv file
    def exportgroups(usrdef_sship, sid):
        show_groups_data = {'offset':0, 'details-level':'full'}
        show_groups_result = ac(usrdef_sship, 443, 'show-groups', show_groups_data ,sid)
        groupsexportfile = open(("exportedgroups.csv"), "w+")
        for group in show_groups_result["objects"]:
            groupsexportfile.write(group["name"] + ",")
            listofmembers = group["members"]
            for member in listofmembers:
                groupsexportfile.write(member["name"] + ";")
            groupsexportfile.write("\n")
        groupsexportfile.close()

class policy:

    #Method to add rule for importrules
    def importaddrules(usrdef_sship, num, name, src, dst, srv, act, sid):
        add_rule_data = {'layer':'Network', 'position':num, 'name':name, 'source':src, 'destination':dst, 'service':srv, 'action':act}
        add_rule_result = ac(usrdef_sship, 443, 'add-access-rule', add_rule_data, sid)

    #Method to import rulebase from csv
    def importrules(usrdef_sship, filename, sid):
        csvrules = open(filename, "r").read().split("\n")
        for line in csvrules:
            if not line:
                continue
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
            policy.importaddrules(usrdef_sship, num, name, src, dst, srv, act, sid)

    #Method to get packages
    def getallpackages(usrdef_sship, sid):
        get_packages_data = {'offset':0, 'details-level':'full'}
        get_packages_result = ac(usrdef_sship, 443, 'show-packages', get_packages_data, sid)
        return (get_packages_result)

    #Method to get layers
    def getalllayers(usrdef_sship, package, sid):
        get_layers_data = {'name':package}
        get_layers_result = ac(usrdef_sship, 443, 'show-package', get_layers_data, sid)
        return (get_layers_result)

    #Method to get export rules
    def exportrules(usrdef_sship, package, layer, sid):
        #Retrieve Rulebase
        show_rulebase_data = {"offset":0, "package":package, "name":layer, "details-level":"standard", "use-object-dictionary":"true"}
        show_rulebase_result = ac(usrdef_sship, 443, 'show-access-rulebase', show_rulebase_data ,sid)
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

class misc:

    #Method to retrieve gateways-and-servers
    def getalltargets(usrdef_sship, sid):
        #Retrieve Targets
        get_targets_data = {'offset':0}
        get_targets_result = ac(usrdef_sship, 443, 'show-gateways-and-servers', get_targets_data ,sid)
        return (get_targets_result)

    #Method to run script
    def runscript(usrdef_sship, target, name, command, sid):
        run_script_data = {'script-name':name, 'script':command, 'targets':target}
        get_targets_result = ac(usrdef_sship, 443, 'run-script', run_script_data , sid)
        for line in get_targets_result["tasks"]:
            taskid = line["task-id"]
        time.sleep(5)
        taskid_data = {'task-id':taskid, 'details-level':'full'}
        taskid_result = ac(usrdef_sship, 443, 'show-task', taskid_data , sid)
        for line in taskid_result["tasks"]:
            taskresult = line["task-details"][0]["statusDescription"]

    #Method to put file
    def putfile(usrdef_sship, target, path, name, contents, sid):
        put_file_data = {'file-path':path, 'file-name':name, 'file-content':contents, 'targets':target}
        put_file_result = ac(usrdef_sship, 443, 'put-file', put_file_data , sid)
