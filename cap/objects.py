from cap.post import api_call


def add_host(apisession, hostname, ipaddress):
    add_host_data = {'name': hostname, 'ipv4-address': ipaddress}
    add_host_response = api_call(apisession.ipaddress, 443, '/add-host',
                                 add_host_data, apisession.sid)
    return add_host_response


def add_network(apisession, netname, network, netmask):
    add_net_data = {'name': netname, 'subnet': network, 'subnet-mask': netmask}
    add_net_response = api_call(apisession.ipaddress, 443, '/add-network',
                                add_net_data, apisession.sid)
    return add_net_response


def add_group(apisession, groupname):
    add_group_data = {'name': groupname}
    add_group_response = api_call(apisession.ipaddress, 443, '/add-group',
                                  add_group_data, apisession.sid)
    return add_group_response


def show_object(apisession, objuid):
    show_obj_data = {'uid': objuid}
    show_obj_response = api_call(apisession.ipaddress, 443, '/show-object',
                                 show_obj_data, apisession.sid)
    type_obj_data = {'uid': objuid, 'details-level': 'full'}
    type_obj_response = api_call(apisession.ipaddress, 443, '/show-{}'.format(
        show_obj_response.json()['object']['type']), type_obj_data,
                                 apisession.sid)
    return type_obj_response
