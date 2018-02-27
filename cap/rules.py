from cap.post import api_call


def get_all_layers(apisession):
    """Retrieve all rule base layers from management server."""
    get_layers_result = api_call(apisession.ipaddress, 443,
                                 'show-access-layers', {}, apisession.sid)
    return [(layer['name'], layer['uid'])
            for layer in get_layers_result.json()['access-layers']]


def dorulebase(rules, rulebase):
    """Recieves json respone of showrulebase and sends rule dictionaries into
    filterpolicyrule."""
    for rule in rulebase.json()['rulebase']:
        if 'type' in rule:
            thetype = rule['type']
            if thetype == 'access-rule':
                filteredrule = filterpolicyrule(rule, rulebase.json())
                rules.append(filteredrule)
        if 'rulebase' in rule:
            for subrule in rule['rulebase']:
                filteredrule = filterpolicyrule(subrule, rulebase.json())
                rules.append(filteredrule)
    return rules


def showrulebase(apisession, layer_uid):
    """Issues API call to manager and holds response of rules until all
    filtering is complete."""
    count = 25
    show_rulebase_data = {
        'uid': layer_uid,
        'details-level': 'standard',
        'offset': 0,
        'limit': 25,
        'use-object-dictionary': 'true'
    }
    show_rulebase_result = api_call(apisession.ipaddress, 443,
                                    'show-access-rulebase', show_rulebase_data,
                                    apisession.sid)

    rules = []

    dorulebase(rules, show_rulebase_result)
    if 'to' in show_rulebase_result.json():
        while show_rulebase_result.json()["to"] != show_rulebase_result.json(
        )["total"]:
            show_rulebase_data = {
                'uid': layer_uid,
                'details-level': 'standard',
                'offset': count,
                'limit': 25,
                'use-object-dictionary': 'true'
            }
            show_rulebase_result = api_call(apisession.ipaddress, 443,
                                            'show-access-rulebase',
                                            show_rulebase_data, apisession.sid)
            dorulebase(rules, show_rulebase_result)
            count += 25

    return rules


def filterpolicyrule(rule, show_rulebase_result):
    """The actual filtering of a rule."""
    filteredrule = {}
    if 'name' in rule:
        name = rule['name']
    else:
        name = ''
    num = rule['rule-number']
    src = rule['source']
    src_all = []
    dst = rule['destination']
    dst_all = []
    dst_uid = rule['destination']
    srv = rule['service']
    srv_all = []
    act = rule['action']
    if rule['track']['type']:
        trc = rule['track']['type']
    else:
        trc = rule['track']
    trg = rule['install-on']
    trg_all = []
    for obj in show_rulebase_result['objects-dictionary']:
        if name == obj['uid']:
            name = obj['name']
        if num == obj['uid']:
            num = obj['name']
        if act == obj['uid']:
            act = obj['name']
        if trc == obj['uid']:
            trc = obj['name']
    for srcobj in src:
        for obj in show_rulebase_result['objects-dictionary']:
            if srcobj == obj['uid']:
                src_all.append((obj['name'], srcobj))
    for dstobj in dst:
        for obj in show_rulebase_result['objects-dictionary']:
            if dstobj == obj['uid']:
                dst_all.append((obj['name'], dstobj))
    for srvobj in srv:
        for obj in show_rulebase_result['objects-dictionary']:
            if srvobj == obj['uid']:
                srv_all.append((obj['name'], srvobj))
    for trgobj in trg:
        for obj in show_rulebase_result['objects-dictionary']:
            if trgobj == obj['uid']:
                trg_all.append((obj['name'], trgobj))
    filteredrule.update({
        'number': num,
        'name': name,
        'source': src_all,
        'source-negate': rule['source-negate'],
        'destination': dst_all,
        'destination-negate': rule['destination-negate'],
        'service': srv_all,
        'service-negate': rule['service-negate'],
        'action': act,
        'track': trc,
        'target': trg_all,
        'enabled': rule['enabled']
    })
    return filteredrule
