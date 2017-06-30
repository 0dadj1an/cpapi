#Import Post
from cpapipackage.post import api_call

#Method to add rule for importrules
def importaddrules(usrdef_sship, num, name, src, dst, srv, act, trc, trg, sid):
    add_rule_data = {'layer':'Network', 'position':num, 'name':name, 'source':src, 'destination':dst, 'service':srv, 'action':act, 'track':trc, 'install-on':trg}
    api_call(usrdef_sship, 443, 'add-access-rule', add_rule_data, sid)

#Method to import rulebase from csv
def importrules(usrdef_sship, filename, sid):
    #Read csv and split format for add command
    csvrules = open(filename, "r").read().split("\n")
    for line in csvrules:
        #This shit is everywhere
        if not line:
            continue
        fullrule = line.split(',')
        num = fullrule[0]
        name = fullrule[1]
        #Some fields can contain multiple objects delimited with ;
        try:
            src = fullrule[2].split(';')
        except:
            src = fullrule[2]
        try:
            dst = fullrule[3].split(';')
        except:
            dst = fullrule[3]
        try:
            srv = fullrule[4].split(';')
        except:
            srv = fullrule[4]
        act = fullrule[5]
        trc = fullrule[6]
        try:
            trg = fullrule[7].split(';')
        except:
            trg = fullrule[7]
        importaddrules(usrdef_sship, num, name, src, dst, srv, act, trc, trg, sid)

#Method to get packages
def getallpackages(usrdef_sship, sid):
    #Form API Payload and Call Post
    get_packages_data = {'limit':500, 'details-level':'full'}
    get_packages_result = api_call(usrdef_sship, 443, 'show-packages', get_packages_data, sid)
    #List to append policy packages to
    allpackagelist = []
    #Iterate over json to export package names
    for package in get_packages_result["packages"]:
        allpackagelist.append(package["name"])
    #Return list to GUI
    return (allpackagelist)

#Method to get layers
def getalllayers(usrdef_sship, package, sid):
    #Form API Payload and Call Post
    get_layers_data = {'name':package}
    get_layers_result = api_call(usrdef_sship, 443, 'show-package', get_layers_data, sid)
    #List to append layers to
    alllayerslist = []
    #Iterate over json for layer names
    for layer in get_layers_result["access-layers"]:
        alllayerslist.append(layer["name"])
    #Return list to GUI
    return (alllayerslist)

#Method to get export rules
def exportrules(usrdef_sship, package, layer, sid):
    #Check if run from gem
    if package == 'package':
        show_rulebase_data = {'package':'Standard', 'name':'Network', 'details-level':'standard', 'use-object-dictionary':'true'}
        show_rulebase_result = api_call(usrdef_sship, 443, 'show-access-rulebase', show_rulebase_data ,sid)
    else:
        #Form API Payload and Call Post
        show_rulebase_data = {'package':package, 'name':layer, 'details-level':'standard', 'use-object-dictionary':'true'}
        show_rulebase_result = api_call(usrdef_sship, 443, 'show-access-rulebase', show_rulebase_data ,sid)
    #Write json result to log file
    logfile = open(("logfile.txt"), "a")
    logfile.write(str(show_rulebase_result) + "\n")
    rulebaseexport = open(("exportedrules.csv"), "w+")
    rulebaseexport.close()
    #Iterate over json to extract rules
    for rule in show_rulebase_result["rulebase"]:
        #Have to check for type first
        if "type" in rule:
            #Save type to varialbe to run check against
            thetype = rule["type"]
            #Call save method if a rule, as apposed to section
            if thetype == "access-rule":
                filterpolicyrule(rule, show_rulebase_result)
        #If sections exist, rulebase will exist in rulebase!!! DUMB CP!
        if "rulebase" in rule:
            for subrule in rule["rulebase"]:
                filterpolicyrule(subrule, show_rulebase_result)

#Method to save policy rule
def filterpolicyrule(rule, show_rulebase_result):
    #HUGE CRAZY MESS I'LL COMMENT ONE DAY!
    rulebaseexport = open(("exportedrules.csv"), "a")
    # Counter for fields which require loops over the objects-dictionary
    countersrc = 0
    counterdst = 0
    countersrv = 0
    countertrg = 0
    # The name field can be absent, check for existence.
    if 'name' in rule:
        name = rule["name"]
    # Give a place holder name if no name existed
    else:
        name = "ASSIGN NAME"
    num = rule["rule-number"]
    src = rule["source"]
    dst = rule["destination"]
    srv = rule["service"]
    act = rule["action"]
    # R80.10 introduced support for other track fields whicl will present in a dictionary
    # Only get the standard log field
    if rule["track"]["type"]:
        trc = rule["track"]["type"]
    else:
        trc = rule["track"]
    trg = rule["install-on"]
    # Consider condensing loops which have no counter into one loop
    for obj in show_rulebase_result["objects-dictionary"]:
        if name == obj["uid"]:
            name = obj["name"]
    for obj in show_rulebase_result["objects-dictionary"]:
        if num == obj["uid"]:
            num = obj["name"]
    # Check if one object in source field or >1
    if len(src) == 1:
        # Source export is saved as list, replace index 0 if only 1
        for obj in show_rulebase_result["objects-dictionary"]:
            if src[0] == obj["uid"]:
                src = obj["name"]
    # If more than one source object
    else:
        # Loop over source list and loop over objects-dictionary and modify corresponding UID index
        for srcobj in src:
            for obj in show_rulebase_result["objects-dictionary"]:
                if srcobj == obj["uid"]:
                    src[countersrc] = obj["name"]
                    countersrc = countersrc + 1
    if len(dst) == 1:
        for obj in show_rulebase_result["objects-dictionary"]:
            if dst[0] == obj["uid"]:
                dst = obj["name"]
    else:
        for dstobj in dst:
            for obj in show_rulebase_result["objects-dictionary"]:
                if dstobj == obj["uid"]:
                    dst[counterdst] = obj["name"]
                    counterdst = counterdst + 1
    if len(srv) == 1:
        for obj in show_rulebase_result["objects-dictionary"]:
            if srv[0] == obj["uid"]:
                srv = obj["name"]
    else:
        for srvobj in srv:
            for obj in show_rulebase_result["objects-dictionary"]:
                if srvobj == obj["uid"]:
                    srv[countersrv] = obj["name"]
                    countersrv = countersrv + 1
    for obj in show_rulebase_result["objects-dictionary"]:
        if act == obj["uid"]:
            act = obj["name"]
    for obj in show_rulebase_result["objects-dictionary"]:
        if trc == obj["uid"]:
            trc = obj["name"]
    if len(trg) == 1:
        for obj in show_rulebase_result["objects-dictionary"]:
            if trg[0] == obj["uid"]:
                trg = obj["name"]
    else:
        for trgobj in trg:
            for obj in show_rulebase_result["objects-dictionary"]:
                if trgobj == obj["uid"]:
                    trg[countertrg] = obj["name"]
                    countertrg = countertrg + 1
    # Begin writing rules to export file
    rulebaseexport.write(str(num) + ',' + name + ',')
    # Verify if only one object or several
    if isinstance(src, str) == True:
        rulebaseexport.write(src + ',')
    # If more than one, write all fields except last which is white space index
    else:
        for srcele in src[0:-1]:
            rulebaseexport.write(srcele + ';')
        rulebaseexport.write(src[-1] + ',')
    if isinstance(dst, str) == True:
        rulebaseexport.write(dst + ',')
    else:
        for dstele in dst[0:-1]:
            rulebaseexport.write(dstele + ';')
        rulebaseexport.write(dst[-1] + ',')
    if isinstance(srv, str) == True:
        rulebaseexport.write(srv + ',')
    else:
        for srvele in srv[0:-1]:
            rulebaseexport.write(srvele + ';')
        rulebaseexport.write(srv[-1] + ',')
    rulebaseexport.write(act + ',')
    rulebaseexport.write(trc + ',')
    if isinstance(trg, str) == True:
        rulebaseexport.write(trg + '\n')
    else:
        for trgele in trg[0:-1]:
            rulebaseexport.write(trgele + ';')
        rulebaseexport.write(trg[-1] + '\n')
    rulebaseexport.close()

#Method to add nat rules for import nat
def importaddnat(usrdef_sship, aut, ena, met, num, osc, ods, osr, tsc, tds, tsr, trg, sid):
    #Can't write to auto section, must use position top to avoid if it's the first rule
    if aut == "False" and num == "1":
        add_rule_data = {'package':'Standard', 'enabled':ena, 'method':met, 'position':'top', 'original-source':osc, 'original-destination':ods,
                        'original-source':osc, 'translated-source':tsc, 'translated-destination':tds, 'translated-service':tsr, 'install-on':trg}
    elif aut == "False" and num !="1":
        add_rule_data = {'package':'Standard', 'enabled':ena, 'method':met, 'position':num, 'original-source':osc, 'original-destination':ods,
                        'original-source':osc, 'translated-source':tsc, 'translated-destination':tds, 'translated-service':tsr, 'install-on':trg}
    api_call(usrdef_sship, 443, 'add-nat-rule', add_rule_data, sid)

#Method to import nat rules from csv
def importnat(usrdef_sship, filename, sid):
    #Read csf and format for add nat rule method
    csvrules = open(filename, "r").read().split("\n")
    for line in csvrules:
        #Hmmmmm
        if not line:
            continue
        fullrule = line.split(',')
        aut = fullrule[0]
        ena = fullrule[1]
        met = fullrule[2]
        num = fullrule[3]
        osc = fullrule[4]
        ods = fullrule[5]
        osr = fullrule[6]
        tsc = fullrule[7]
        tds = fullrule[8]
        tsr = fullrule[9]
        #Some fields can have more than one object!
        try:
            trg = fullrule[10].split(';')
        except:
            trg = fullrule[10]
        #Only add rule if not auto generated by objects
        if aut == "False":
            importaddnat(usrdef_sship, aut, ena, met, num, osc, ods, osr, tsc, tds, tsr, trg, sid)

#Method to export manual nat rules
def exportnat(usrdef_sship, package, sid):
    #Check if from gem
    if package == 'package':
        show_natrulebase_data = {'package':'Standard', 'details-level':'standard', 'use-object-dictionary':'true'}
        show_natrulebase_result = api_call(usrdef_sship, 443, 'show-nat-rulebase', show_natrulebase_data ,sid)
    else:
        #Form API Payload and Call Post
        show_natrulebase_data = {'package':package, 'details-level':'standard', 'use-object-dictionary':'true'}
        show_natrulebase_result = api_call(usrdef_sship, 443, 'show-nat-rulebase', show_natrulebase_data ,sid)
    #Write json response to log file
    logfile = open(("logfile.txt"), "a")
    logfile.write(str(show_natrulebase_result) + "\n")
    natrulebasefile = open(("exportednatrules.csv"), "w+")
    natrulebasefile.close()
    #Iterate over json for rule info
    for rule in show_natrulebase_result["rulebase"]:
        #Must check for type first
        if "type" in rule:
            #Save type to variable to run if against
            thetype = rule["type"]
            #As apposed to section
            if thetype == "nat-rule":
                #Call method to save info
                filternatrule(rule, show_natrulebase_result)
        #When sections exist, we have rulebase inside of rulebase! Such naming scheme, very wow!
        if "rulebase" in rule:
            for subrule in rule["rulebase"]:
                filternatrule(subrule, show_natrulebase_result)

def filternatrule(rule, show_natrulebase_result):
    #ONE DAY, I'll COMMENT THIS MESS!
    natrulebasefile = open(("exportednatrules.csv"), "a")
    countertrg = 0
    aut = rule["auto-generated"]
    ena = rule["enabled"]
    met = rule["method"]
    num = rule["rule-number"]
    osc = rule["original-source"]
    ods = rule["original-destination"]
    osr = rule["original-service"]
    tsc = rule["translated-source"]
    tds = rule["translated-destination"]
    tsr = rule["translated-service"]
    trg = rule["install-on"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if num == obj["uid"]:
            num = obj["name"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if osc == obj["uid"]:
            osc = obj["name"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if ods == obj["uid"]:
            ods = obj["name"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if osr == obj["uid"]:
            osr = obj["name"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if tsc == obj["uid"]:
            tsc = obj["name"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if tds == obj["uid"]:
            tds = obj["name"]
    for obj in show_natrulebase_result["objects-dictionary"]:
        if tsr == obj["uid"]:
            tsr = obj["name"]
    if len(trg) == 1:
        for obj in show_natrulebase_result["objects-dictionary"]:
            if trg[0] == obj["uid"]:
                trg = obj["name"]
    else:
        for trgobj in trg:
            for obj in show_natrulebase_result["objects-dictionary"]:
                if trgobj == obj["uid"]:
                    trg[countertrg] = obj["name"]
                    countertrg = countertrg + 1
    natrulebasefile.write("{},{},{},{},{},{},{},{},{},{},".format(aut, ena, met, num, osc, ods, osr, tsc, tds, tsr))
    if isinstance(trg, str) == True:
        natrulebasefile.write(trg + '\n')
    else:
        for trgele in trg[0:-1]:
            natrulebasefile.write(trgele + ';')
        natrulebasefile.write(trg[-1] + '\n')
    natrulebasefile.close()
