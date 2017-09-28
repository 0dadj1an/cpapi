#Import Post
from cpapipackage.post import api_call

#Method to retrieve gateways-and-servers
def getalltargets(usrdef_sship, sid):
    #Form API Payload and Call Post
    get_targets_data = {'limit':500}
    get_targets_result = api_call(usrdef_sship, 443, 'show-gateways-and-servers', get_targets_data ,sid)
    #List to append target gw and mgmt to
    targetslist = []
    #Iterate over json response for targe name only
    for obj in get_targets_result["objects"]:
        targetslist.append(obj["name"])
    #Return list to gui
    return (targetslist)

#Method to run script
def runcommand(usrdef_sship, target, name, command, sid):
    #Form API Payload and Call Post
    run_script_data = {'script-name':name, 'script':command, 'targets':target}
    api_call(usrdef_sship, 443, 'run-script', run_script_data , sid)

#Method to put file
def putfile(usrdef_sship, target, path, name, contents, sid):
    #Form API Payload and Call Post
    put_file_data = {'file-path':path, 'file-name':name, 'file-content':contents, 'targets':target}
    api_call(usrdef_sship, 443, 'put-file', put_file_data , sid)

#Method to run costom command
def customcommand(userdef_sship, command, payload, sid):
    #Form API Payload
    payload = eval(payload)
    custcomm_data = payload
    api_call(userdef_sship, 443, command, custcomm_data, sid)

def getallcommands(usrdef_sship, sid):
    #Form API Payload
    commandlist = []
    getcommands_data = {}
    getcommands_result = api_call(usrdef_sship, 443, 'show-commands', getcommands_data, sid)
    for obj in getcommands_result["commands"]:
        commandlist.append(obj["name"])
    return(commandlist)
