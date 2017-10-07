from cap.post import api_call

def addgroup(ipaddress, groupname, sid):
    new_group_data = {'name':groupname}
    response = api_call(ipaddress, 443, 'add-group', new_group_data ,sid)
    return(response)

def setgroup(ipaddress, groupname, members, sid):
    set_group_data = {'name':groupname, 'members':{'add':members}}
    response = api_call(ipaddress, 443, 'set-group', set_group_data, sid)
    return(response)

def importgroups(ipaddress, filename, sid):
    report = []
    csvgroups = open(filename, 'r').read().split('\n')
    for line in csvgroups:
        if not line:
            continue
        groupname = line.split(';')
        memberlist = groupname[1].split(',')
        response = importaddgroup(ipaddress, groupname[0], memberlist[0:-1], sid)
        if response.status_code == 200:
            report.append('Host:{} - SUCCESS'.format(groupname[0]))
        else:
            report.append('Host:{} - FAILURE'.format(groupname[0]))
    return(report)

def importaddgroup(ipaddress, groupname, members, sid):
    import_group_data = {'name':groupname, 'members':members}
    response = api_call(ipaddress, 443, 'add-group', import_group_data, sid)
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
