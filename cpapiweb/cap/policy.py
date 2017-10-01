from cap.post import api_call

def showrulebase(ipaddress, name, sid):
    show_rulebase_data = {'name':name, 'details-level':'standard', 'use-object-dictionary':'true'}
    show_rulebase_result = api_call(ipaddress, 443, 'show-access-rulebase', show_rulebase_data ,sid)

    rules = []
    for rule in show_rulebase_result['rulebase']:
        if 'type' in rule:
            thetype = rule['type']
            if thetype == 'access-rule':
                filteredrule = filterpolicyrule(rule, show_rulebase_result)
                rules.append(filteredrule)
        if 'rulebase' in rule:
            for subrule in rule['rulebase']:
                filteredrule = filterpolicyrule(subrule, show_rulebase_result)
                rules.append(filteredrule)
    return(rules)

def filterpolicyrule(rule, show_rulebase_result):
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
    if len(src) == 1:
        for obj in show_rulebase_result['objects-dictionary']:
            if src[0] == obj['uid']:
                src = obj['name']
    else:
        for srcobj in src:
            for obj in show_rulebase_result['objects-dictionary']:
                if srcobj == obj['uid']:
                    src[countersrc] = obj['name']
                    countersrc = countersrc + 1
    if len(dst) == 1:
        for obj in show_rulebase_result['objects-dictionary']:
            if dst[0] == obj['uid']:
                dst = obj['name']
    else:
        for dstobj in dst:
            for obj in show_rulebase_result['objects-dictionary']:
                if dstobj == obj['uid']:
                    dst[counterdst] = obj['name']
                    counterdst = counterdst + 1
    if len(srv) == 1:
        for obj in show_rulebase_result['objects-dictionary']:
            if srv[0] == obj['uid']:
                srv = obj['name']
    else:
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
    if len(trg) == 1:
        for obj in show_rulebase_result['objects-dictionary']:
            if trg[0] == obj['uid']:
                trg = obj['name']
    else:
        for trgobj in trg:
            for obj in show_rulebase_result['objects-dictionary']:
                if trgobj == obj['uid']:
                    trg[countertrg] = obj['name']
                    countertrg = countertrg + 1
    filteredrule.update({'number':num, 'name':name, 'source':src, 'destination':dst, 'service':srv, 'action':act, 'track':trc, 'target':trg})
    return(filteredrule)
