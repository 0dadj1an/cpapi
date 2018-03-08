from cap.post import api_call


def addhost(apisession, hostpayload):
    add_host_response = api_call(apisession.ipaddress, 443, 'add-host',
                                 hostpayload, apisession.sid)
    return add_host_response


def addnetwork(apisession, netpayload):
    add_net_response = api_call(apisession.ipaddress, 443, 'add-network',
                                netpayload, apisession.sid)
    return add_net_response


def addgroup(apisession, groupname):
    add_group_data = {'name': groupname}
    add_group_response = api_call(apisession.ipaddress, 443, 'add-group',
                                  add_group_data, apisession.sid)
    return add_group_response


def show_object(apisession, objuid):
    show_obj_data = {'uid': objuid}
    show_obj_response = api_call(apisession.ipaddress, 443, 'show-object',
                                 show_obj_data, apisession.sid)
    type_obj_data = {'uid': objuid, 'details-level': 'full'}
    type_obj_response = api_call(apisession.ipaddress, 443, 'show-{}'.format(
        show_obj_response.json()['object']['type']), type_obj_data,
                                 apisession.sid)
    return type_obj_response
