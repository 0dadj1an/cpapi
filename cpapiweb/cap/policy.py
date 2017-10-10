from cap.post import api_call

def getalllayers(ipaddress, sid):
    '''Retrieve all rule base layers from management server.'''
    get_layers_data = {}
    get_layers_result = api_call(ipaddress, 443, 'show-access-layers', get_layers_data, sid)
    alllayerslist = []
    for layer in get_layers_result.json()['access-layers']:
        alllayerslist.append(layer['name'])
    return (alllayerslist)

def dorulebase(rules, rulebase):
    '''Recieves json respone of showrulebase and sends rule dictionaries int filterpolicyrule.'''
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
    return(rules)

def showrulebase(ipaddress, name, sid):
    '''Issues API call to manager and holds response of rules until all filtering is complete.'''
    count = 500
    show_rulebase_data = {'name':name, 'details-level':'standard', 'offset':0, 'limit':500, 'use-object-dictionary':'true'}
    show_rulebase_result = api_call(ipaddress, 443, 'show-access-rulebase', show_rulebase_data ,sid)

    rules = []

    dorulebase(rules, show_rulebase_result)
    if 'to' in show_rulebase_result.json():
        while show_rulebase_result.json()["to"] != show_rulebase_result.json()["total"]:
            show_rulebase_data = {'name':name, 'details-level':'standard', 'offset':count, 'limit':500, 'use-object-dictionary':'true'}
            show_rulebase_result = api_call(ipaddress, 443, 'show-access-rulebase', show_rulebase_data ,sid)
            dorulebase(rules, show_rulebase_result)
            count += 500

    return(rules)

def filterpolicyrule(rule, show_rulebase_result):
    '''The actually filtering of a rule.'''
    filteredrule = {}
    countersrc = 0
    counterdst = 0
    countersrv = 0
    countertrg = 0
    if 'name' in rule:
        name = rule['name']
    else:
        name = ''
    num = rule['rule-number']
    src = rule['source']
    dst = rule['destination']
    srv = rule['service']
    act = rule['action']
    if rule['track']['type']:
        trc = rule['track']['type']
    else:
        trc = rule['track']
    trg = rule['install-on']
    for obj in show_rulebase_result['objects-dictionary']:
        if name == obj['uid']:
            name = obj['name']
    for obj in show_rulebase_result['objects-dictionary']:
        if num == obj['uid']:
            num = obj['name']
    for srcobj in src:
        for obj in show_rulebase_result['objects-dictionary']:
            if srcobj == obj['uid']:
                src[countersrc] = obj['name']
                countersrc = countersrc + 1
    for dstobj in dst:
        for obj in show_rulebase_result['objects-dictionary']:
            if dstobj == obj['uid']:
                dst[counterdst] = obj['name']
                counterdst = counterdst + 1
    for srvobj in srv:
        for obj in show_rulebase_result['objects-dictionary']:
            if srvobj == obj['uid']:
                srv[countersrv] = obj['name']
                countersrv = countersrv + 1
    for obj in show_rulebase_result['objects-dictionary']:
        if act == obj['uid']:
            act = obj['name']
    for obj in show_rulebase_result['objects-dictionary']:
        if trc == obj['uid']:
            trc = obj['name']
    for trgobj in trg:
        for obj in show_rulebase_result['objects-dictionary']:
            if trgobj == obj['uid']:
                trg[countertrg] = obj['name']
                countertrg = countertrg + 1
    filteredrule.update({'number':num, 'name':name, 'source':src,
                        'destination':dst, 'service':srv, 'action':act,
                        'track':trc, 'target':trg})
    return(filteredrule)
