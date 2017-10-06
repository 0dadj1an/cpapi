from cap.post import api_call

def addgroup(ipaddress, groupname, sid):
    new_group_data = {'name':groupname}
    response = api_call(ipaddress, 443,'add-group', new_group_data ,sid)
    return(response)

def setgroup(ipaddress, groupname, members, sid):
    set_group_data = {'name':groupname, 'members':members}
    response = api_call(ipaddress, 443, 'set-group', set_group_data, sid)
    return(response)

def getallgroups(ipaddress, sid):
    count = 500
    show_groups_data = {'offset':0, 'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
    show_groups_result = api_call(ipaddress, 443, 'show-groups', show_groups_data, sid)
    allgrouplist = []
    for groups in show_groups_result.json()["objects"]:
        allgrouplist.append(groups["name"])
    if 'to' in show_groups_result:
        while show_groups_result.json()["to"] != show_groups_result.json()["total"]:
            show_groups_data = {'offset':count, 'limit':500, 'details-level':'standard', 'order':[{'ASC':'name'}]}
            show_groups_result = api_call(ipaddress, 443, 'show-groups', show_groups_data, sid)
            for groups in show_groups_result.json()["objects"]:
                allgrouplist.append(groups["name"])
            count = count + 500
    return (allgrouplist)
