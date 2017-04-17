#Import Post
from apipackage.post import api_call
#Import
import sys

#Method to add rule for importrules
def importaddrules(usrdef_sship, num, name, src, dst, srv, act, sid):
    add_rule_data = {'layer':'Network', 'position':num, 'name':name, 'source':src, 'destination':dst, 'service':srv, 'action':act}
    add_rule_result = api_call(usrdef_sship, 443, 'add-access-rule', add_rule_data, sid)

#Method to import rulebase from csv
def importrules(usrdef_sship, filename, sid):
    csvrules = open(filename, "r").read().split("\n")
    for line in csvrules:
        if not line:
            continue
        fullrule = line.split(',')
        num = fullrule[0]
        name = fullrule[1]
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
        importaddrules(usrdef_sship, num, name, src, dst, srv, act, sid)

#Method to get packages
def getallpackages(usrdef_sship, sid):
    get_packages_data = {'offset':0, 'details-level':'full'}
    get_packages_result = api_call(usrdef_sship, 443, 'show-packages', get_packages_data, sid)
    allpackagelist = []
    for package in get_packages_result["packages"]:
        allpackagelist.append(package["name"])
    return (allpackagelist)

#Method to get layers
def getalllayers(usrdef_sship, package, sid):
    get_layers_data = {'name':package}
    get_layers_result = api_call(usrdef_sship, 443, 'show-package', get_layers_data, sid)
    alllayerslist = []
    for layer in get_layers_result["access-layers"]:
        alllayerslist.append(layer["name"])
    return (alllayerslist)

#Method to get export rules
def exportrules(usrdef_sship, package, layer, sid):
    show_rulebase_data = {"offset":0, "package":package, "name":layer, "details-level":"standard", "use-object-dictionary":"true"}
    show_rulebase_result = api_call(usrdef_sship, 443, 'show-access-rulebase', show_rulebase_data ,sid)
    rulebaseexport = open(("exportedrules.csv"), "w+")
    for rule in show_rulebase_result["rulebase"]:
        countersrc = 0
        counterdst = 0
        countersrv = 0
        if 'name' in rule:
            name = rule["name"]
        else:
            name = "ASSIGN NAME"
        num = rule["rule-number"]
        src = rule["source"]
        dst = rule["destination"]
        srv = rule["service"]
        act = rule["action"]
        for obj in show_rulebase_result["objects-dictionary"]:
            if name == obj["uid"]:
                name = obj["name"]
        for obj in show_rulebase_result["objects-dictionary"]:
            if num == obj["uid"]:
                num = obj["name"]
        if len(src) == 1:
            for obj in show_rulebase_result["objects-dictionary"]:
                if src[0] == obj["uid"]:
                    src = obj["name"]
        else:
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
        rulebaseexport.write(str(num) + ',' + name + ',')
        if isinstance(src, str) == True:
            rulebaseexport.write(src + ',')
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
        rulebaseexport.write(act + '\n')
    rulebaseexport.close()
