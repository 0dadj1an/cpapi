#Import Post
from apipackage.post import api_call

#Method to export host to csv file
def exporttcpservices(usrdef_sship, sid):
    show_tcp_data = {'offset':0, 'details-level':'full'}
    show_tcp_result = api_call(usrdef_sship, 443, 'show-services-tcp', show_tcp_data ,sid)
    print (show_tcp_result)
    tcpexport = open(("exportedtcpsrv.csv"), "w+")
    for service in show_tcp_result["objects"]:
        if service["domain"]["name"] == 'SMC User':
            tcpexport.write(service["name"] + ";" + str(service["port"]) + ";" + str(service["keep-connections-open-after-policy-installation"]) + ";" +
                            str(service["session-timeout"]) + ";" + str(service["match-for-any"]) + ";" + str(service["sync-connections-on-cluster"]) + ";" +
                            str(service["aggressive-aging"]) + "\n")
        elif service["domain"]["name"] == 'Check Point Data':
            break
        else:
            print ("uh oh")
    tcpexport.close()

#Method for adding tcp service for importtcpservice
def importaddtcp(usrdef_sship, name, port, kcoapi, st, mfa, sync, aa, sid):
    aa = eval(aa)
    new_tcp_data = {'name':name, 'port':port, 'keep-connections-open-after-policy-installation':kcoapi, 'session-timeout':st, 'match-for-any':mfa,
                    'sync-connections-on-cluster':sync, 'aggressive-aging':aa}
    api_call(usrdef_sship, 443, 'add-service-tcp', new_tcp_data, sid)

#Method to import tcp service from csv file
def importtcpservice(usrdef_sship, filename, sid):
    csvtcp = open(filename, "r").read().split("\n")
    for line in csvtcp:
        if not line:
            continue
        apiprep = line.split(';')
        importaddtcp(usrdef_sship, apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4], apiprep[5], apiprep[6], sid)
