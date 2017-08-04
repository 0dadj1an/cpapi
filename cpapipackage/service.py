#Import Post
from cpapipackage.post import api_call
import json

#Method to export tcp services to csv file
def exporttcpservices(usrdef_sship, sid):
    #Form API Payload and Call Post
    show_tcp_data = {'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
    show_tcp_result = api_call(usrdef_sship, 443, 'show-services-tcp', show_tcp_data ,sid)
    #Write json output to log file
    tcpexport = open(("exportedtcpsrv.csv"), "w+")
    #Iterate over json response for service info
    for service in show_tcp_result["objects"]:
        #Check if user created or default service
        if service["domain"]["name"] == 'SMC User':
            #Check if value exist for source-port, not present in data otherwise
            if 'source-port' in service:
                sp = service["source-port"]
            else:
                sp = 'none'
            #Check for protocol, no proto if no proto
            if 'protocol' in service:
                proto = service["protocol"]
            else:
                proto = 'none'
            #Write fields to files
            tcpexport.write(service["name"] + ";" + str(service["port"]) + ";" + str(service["keep-connections-open-after-policy-installation"]) + ";" +
                            str(service["session-timeout"]) + ";" + str(sp) + ";" + str(service["match-for-any"]) + ";" +
                            str(service["sync-connections-on-cluster"]) + ";" + service["color"] + ";" + str(service["match-by-protocol-signature"]) + ";" +
                            str(service["override-default-settings"]) + ";" + str(service["use-default-session-timeout"]) + ";" + proto + ";" +
                            str(service["aggressive-aging"]) + "\n")
        elif service["domain"]["name"] == 'Check Point Data':
            continue
        else:
            print ("uh oh")
    tcpexport.close()

#Method for adding tcp service for importtcpservice
def importaddtcp(usrdef_sship, name, port, kcoapi, st, sp, mfa, sync, srvcol, mbps, ods, udst, proto, aa, sid):
    #AA comes in as string, eval for dictionary
    aa = eval(aa)
    #Payload decision based on sp and proto
    if sp == 'none' and proto == 'none':
        new_tcp_data = {'name':name, 'port':port, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'match-for-any':mfa,
                        'sync-connections-on-cluster':sync, 'color':srvcol, 'match-by-protocol-signature':mbps, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'aggressive-aging':aa}
    elif sp == 'none' and proto != 'none':
        new_tcp_data = {'name':name, 'port':port, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st,
                        'match-for-any':mfa, 'sync-connections-on-cluster':sync, 'color':srvcol, 'match-by-protocol-signature':mbps, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'protocol':proto, 'aggressive-aging':aa}
    elif sp != 'none' and proto == 'none':
        new_tcp_data = {'name':name, 'port':port, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'source-port':sp,
                        'match-for-any':mfa, 'sync-connections-on-cluster':sync, 'color':srvcol, 'match-by-protocol-signature':mbps, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'aggressive-aging':aa}
    else:
        new_tcp_data = {'name':name, 'port':port, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'source-port':sp,
                        'match-for-any':mfa, 'sync-connections-on-cluster':sync, 'color':srvcol, 'match-by-protocol-signature':mbps, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'protocol':proto, 'aggressive-aging':aa}
    api_call(usrdef_sship, 443, 'add-service-tcp', new_tcp_data, sid)

#Method to import tcp service from csv file
def importtcpservice(usrdef_sship, filename, sid):
    csvtcp = open(filename, "r").read().split("\n")
    for line in csvtcp:
        #Nobody knoooooooows
        if not line:
            continue
        apiprep = line.split(';')
        importaddtcp(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4], apiprep[5],
                     apiprep[6], apiprep[7], apiprep[8], apiprep[9], apiprep[10], apiprep[11], apiprep[12], sid)

#Method to export udp services to csv file
def exportudpservices(usrdef_sship, sid):
    #Form API Payload and Call Post
    show_udp_data = {'limit':500, 'details-level':'full', 'order':[{'ASC':'name'}]}
    show_udp_result = api_call(usrdef_sship, 443, 'show-services-udp', show_udp_data ,sid)
    #Write json result to log file
    udpexport = open(("exportedudpsrv.csv"), "w+")
    #Iterate over json to extract services
    for service in show_udp_result["objects"]:
        #Check if created by user or default object
        if service["domain"]["name"] == 'SMC User':
            #Check for source-port, otherwise it doesn't exist
            if 'source-port' in service:
                sp = service["source-port"]
            else:
                sp = 'none'
            #Check for protocol, no proto if no proto
            if 'protocol' in service:
                proto = service["protocol"]
            else:
                proto = 'none'
            #Write that data to the file my man
            udpexport.write(service["name"] + ";" + str(service["port"]) + ";" + str(service["accept-replies"]) + ";" +
                            str(service["keep-connections-open-after-policy-installation"]) + ";" +
                            str(service["session-timeout"]) + ";" + str(sp) + ";" + str(service["match-for-any"]) + ";" +
                            str(service["sync-connections-on-cluster"]) + ";" + service["color"] + ";" + proto + ";" +
                            str(service["override-default-settings"]) + ";" + str(service["use-default-session-timeout"]) + ";" +
                            str(service["match-by-protocol-signature"]) + ";" + str(service["aggressive-aging"]) + "\n")
        #Break loop if default object
        elif service["domain"]["name"] == 'Check Point Data':
            continue
        #You never know.
        else:
            print ("uh oh")
    udpexport.close()

#Method for adding udp service for importudpservice
def importaddudp(usrdef_sship, name, port, ar, kcoapi, st, sp, mfa, sync, srvcol, proto, ods, udst, mbps, aa, sid):
    #AA comes in as string, eval for dictionary
    aa = eval(aa)
    #Check for SP and proto to formulate proper API payload
    if sp == 'none' and proto == 'none':
        new_udp_data = {'name':name, 'port':port, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'match-for-any':mfa,
                        'sync-connections-on-cluster':sync, 'color':srvcol, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'match-by-protocol-signature':mbps, 'aggressive-aging':aa}
    elif sp == 'none' and proto != 'none':
        new_udp_data = {'name':name, 'port':port, 'accept-replies':ar, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st,
                        'match-for-any':mfa, 'sync-connections-on-cluster':sync, 'color':srvcol, 'protocol':proto, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'match-by-protocol-signature':mbps, 'aggressive-aging':aa}
    elif sp != 'none' and proto == 'none':
        new_udp_data = {'name':name, 'port':port, 'accept-replies':ar, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'source-port':sp,
                'match-for-any':mfa, 'sync-connections-on-cluster':sync, 'color':srvcol, 'override-default-settings':ods,
                'use-default-session-timeout':udst, 'match-by-protocol-signature':mbps, 'aggressive-aging':aa}
    else:
        new_udp_data = {'name':name, 'port':port, 'accept-replies':ar, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'source-port':sp,
                        'match-for-any':mfa, 'sync-connections-on-cluster':sync, 'color':srvcol, 'protocol':proto, 'override-default-settings':ods,
                        'use-default-session-timeout':udst, 'match-by-protocol-signature':mbps, 'aggressive-aging':aa}
    api_call(usrdef_sship, 443, 'add-service-udp', new_udp_data, sid)

#Method to import udp service from csv file
def importudpservice(usrdef_sship, filename, sid):
    csvudp = open(filename, "r").read().split("\n")
    for line in csvudp:
        #One day, I'll know
        if not line:
            continue
        apiprep = line.split(';')
        importaddudp(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4], apiprep[5], apiprep[6], apiprep[7],
                     apiprep[8], apiprep[9], apiprep[10], apiprep[11], apiprep[12], apiprep[13], sid)
