#Import Post
from post import api_call
#Import
import sys

class group:

    #Method for adding a group object
    def addgroup(usrdef_sship, groupname, sid):
        new_group_data = {'name':groupname}
        new_group_result = post.api_call(usrdef_sship, 443,'add-group', new_group_data ,sid)

    #Method to add group to group
    def addgroupgroup(usrdef_sship, addgroupname, groupname, sid):
        addgroup_data = {'name':addgroupname, 'groups':groupname}
        addgroupgroup_result = post.api_call(usrdef_sship, 443, 'set-group', addgroup_data, sid)

    #Method for retrieving all groups
    def getallgroups(usrdef_sship, sid):
        show_groups_data = {'offset':0, 'details-level':'standard'}
        show_groups_result = post.api_call(usrdef_sship, 443, 'show-groups', show_groups_data, sid)
        return (show_groups_result)

    #Method for adding a group object with members
    def addgroupmembers(usrdef_sship, groupname, members, sid):
        new_group_data = {'name':groupname, 'members':members}
        new_group_result = post.api_call(usrdef_sship, 443,'add-group', new_group_data ,sid)

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
        show_groups_result = post.api_call(usrdef_sship, 443, 'show-groups', show_groups_data ,sid)
        groupsexportfile = open(("exportedgroups.csv"), "w+")
        for group in show_groups_result["objects"]:
            groupsexportfile.write(group["name"] + ",")
            listofmembers = group["members"]
            for member in listofmembers:
                groupsexportfile.write(member["name"] + ";")
            groupsexportfile.write("\n")
        groupsexportfile.close()
