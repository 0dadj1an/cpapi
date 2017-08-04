#Import Post
from cpapipackage.post import api_call
import threading, time, json

#Method for adding a group object
def addgroup(usrdef_sship, groupname, groupcolor, sid):
    #Form API Payload and Call Post
    new_group_data = {'name':groupname, 'color':groupcolor}
    api_call(usrdef_sship, 443,'add-group', new_group_data ,sid)

#Method to add group to group
def addgroupgroup(usrdef_sship, addgroupname, groupname, sid):
    #Form API Payload and Call Post
    addgroup_data = {'name':addgroupname, 'groups':groupname}
    api_call(usrdef_sship, 443, 'set-group', addgroup_data, sid)

#Method for retrieving all groups
def getallgroups(usrdef_sship, sid):
    #Variable for offset if more than 500 objects
    count = 500
    #Form API Payload and Call Post
    show_groups_data = {'offset':0, 'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_groups_result = api_call(usrdef_sship, 443, 'show-groups', show_groups_data, sid)
    #List for retrieval of group names
    allgrouplist = []
    #Extract group name from json response
    for groups in show_groups_result["objects"]:
        allgrouplist.append(groups["name"])
    #Until retrieved all objects if more than 500
    if 'to' in show_groups_result:
        while show_groups_result["to"] != show_groups_result["total"]:
            show_groups_data = {'offset':count, 'limit':500, 'details-level':'standard'}
            show_groups_result = api_call(usrdef_sship, 443, 'show-groups', show_groups_data, sid)
            for groups in show_groups_result["objects"]:
                allgrouplist.append(groups["name"])
            count = count + 500
    #Return list to display in gui
    return (allgrouplist)

#Method for adding a group object with members
def addgroupmembers(usrdef_sship, groupname, members, sid):
    #Form API Payload and Call Post
    #Thread to add 2 per second
    #Had trouble going faster with machines
    #with lower performance
    new_group_data = {'name':groupname, 'members':members}
    t1 = threading.Thread(target=api_call, args=(usrdef_sship, 443, 'add-group', new_group_data ,sid))
    t1.start()
    time.sleep(0.5)

#Method to import group from csv
def importgroups(usrdef_sship, filename, sid):
    csvgroups = open(filename, "r").read().split()
    #Read data from CSV and form for add group call
    for line in csvgroups:
        #Don't remember why I wrote this part
        if not line:
            continue
        groupname = line.split(',')
        memberlist = groupname[1].split(';')
        addgroupmembers(usrdef_sship, groupname[0], memberlist[0:-1], sid)

#Method to export host to csv file
def exportgroups(usrdef_sship, sid):
    #Variable for offset if more than 500 objects
    count = 500
    #Form API Payload and Call Post
    show_groups_data = {'offset':0, 'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
    show_groups_result = api_call(usrdef_sship, 443, 'show-groups', show_groups_data ,sid)
    groupsexportfile = open(("exportedgroups.csv"), "w+")
    #Iterate over response to collect group name and members
    for group in show_groups_result["objects"]:
        #Write group name
        groupsexportfile.write(group["name"] + ",")
        listofmembers = group["members"]
        #Write group members
        for member in listofmembers:
            groupsexportfile.write(member["name"] + ";")
        groupsexportfile.write("\n")
    #Continue until all objects retrieved
    if 'to' in show_groups_result:
        while show_groups_result["to"] != show_groups_result["total"]:
            show_groups_data = {'offset':count, 'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
            show_groups_result = api_call(usrdef_sship, 443, 'show-groups', show_groups_data ,sid)
            for group in show_groups_result["objects"]:
                groupsexportfile.write(group["name"] + ",")
                listofmembers = group["members"]
                for member in listofmembers:
                    groupsexportfile.write(member["name"] + ";")
                groupsexportfile.write("\n")
            count = count + 500
    groupsexportfile.close()
