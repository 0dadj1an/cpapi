#Import
import sys

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
