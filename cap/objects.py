from cap.post import api_call


def add_host(apisession, hostname, ipaddress):
    add_host_data = {'name': hostname, 'ipv4-address': ipaddress}
    add_host_response = api_call(apisession.ipaddress, 443, '/add-host', add_host_data, apisession.sid)
    return add_host_response


def add_network(apisession, netname, network, netmask):
    add_net_data = {'name': netname, 'subnet': network, 'subnet-mask': netmask}
    add_net_response = api_call(apisession.ipaddress, 443, '/add-network', add_net_data, apisession.sid)
    return add_net_response
